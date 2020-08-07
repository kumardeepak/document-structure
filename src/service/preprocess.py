import pandas as pd
from configs.config import  preprocess_config


def cut_page(page_df ,height ,cut_at ,direction):

    cut_mark = height * cut_at
    if direction == 'above':
        sub_df = page_df[page_df['text_top'] <= cut_mark ]

    else :
        sub_df = page_df[page_df['text_top'] >= cut_mark ]

    return sub_df


def add_box_coordinates(sub_df):
    sub_df['text_right']  = sub_df['text_left'] + sub_df['text_width']
    sub_df['text_bottom'] = sub_df['text_top'] + sub_df['text_height']
    return sub_df

def bb_intersection_over_union(rowA, rowB):
    boxA = [rowA['text_left'] ,rowA['text_top'], rowA['text_right'], rowA['text_bottom']]
    boxB = [rowB['text_left'], rowB['text_top'], rowB['text_right'], rowB['text_bottom']]

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


def find_header(xml_dfs, preprocess_config,page_height):
    pdf_levle = []

    page_df = xml_dfs[0]
    sub_df = cut_page(page_df, page_height, cut_at=preprocess_config['header_cut'], direction='above')
    sub_df = add_box_coordinates(sub_df)

    for page2_df in xml_dfs:
        s_df = cut_page(page2_df, page_height, cut_at=preprocess_config['header_cut'], direction='above')
        s_df = add_box_coordinates(s_df)

        page_level = []
        for index1, row1 in sub_df.iterrows():
            iou = 0
            for index2, row2 in s_df.iterrows():
                iou += bb_intersection_over_union(row1, row2)

            page_level.append(iou)
        pdf_levle.append(page_level)

    iou_df = pd.DataFrame(pdf_levle, columns=sub_df['text'].values)
    check_repeation = iou_df.sum() / len(iou_df)
    regions_to_remove = sub_df[list(check_repeation > preprocess_config['repeat_threshold'])]

    return regions_to_remove


def find_footer(xml_dfs, preprocess_config,page_height):
    pdf_levle = []

    page_df = xml_dfs[0]
    sub_df = cut_page(page_df, page_height, cut_at=preprocess_config['footer_cut'], direction='below')
    sub_df = add_box_coordinates(sub_df)

    for page2_df in xml_dfs:
        s_df = cut_page(page2_df, page_height, cut_at=preprocess_config['footer_cut'], direction='below')
        s_df = add_box_coordinates(s_df)

        page_level = []
        for index1, row1 in sub_df.iterrows():
            iou = 0
            for index2, row2 in s_df.iterrows():
                iou += bb_intersection_over_union(row1, row2)

            page_level.append(iou)
        pdf_levle.append(page_level)

    iou_df = pd.DataFrame(pdf_levle, columns=sub_df['text'].values)
    check_repeation = iou_df.sum() / len(iou_df)
    regions_to_remove = sub_df[list(check_repeation > preprocess_config['repeat_threshold'])]

    return regions_to_remove


def add_attrib(page_df, region_to_change, attrib, margin=5):
    if len(region_to_change) > 0:
        for index, row in region_to_change.iterrows():
            area = [row['text_top'] - margin, row['text_left'] - margin, row['text_top'] + row['text_height'] + margin,
                    row['text_left'] + row['text_width'] + margin]
            #print(area)
            #print((page_df['text_top'] >= area[0]) & (page_df['text_left'] >= area[1]) & (
            #            page_df['text_top'] + page_df['text_height'] <= area[2]) & (
            #                  page_df['text_left'] + page_df['text_width'] <= area[3]))
            page_df['attrib'][(page_df['text_top'] >= area[0]) & (page_df['text_left'] >= area[1]) & (
                        page_df['text_top'] + page_df['text_height'] <= area[2]) & (
                                          page_df['text_left'] + page_df['text_width'] <= area[3])] = attrib

    return page_df


def prepocess_pdf_rgions(xml_dfs,page_height,config =preprocess_config ):
    header_region = find_header(xml_dfs, config,page_height)
    footer_region = find_footer(xml_dfs, config,page_height)

    return header_region , footer_region

def tag_heaader_footer_attrib(header_region , footer_region ,page_df,magrin=5):
    page_df  = add_attrib(page_df, header_region ,attrib='HEADER',margin=magrin)
    page_df = add_attrib(page_df, footer_region, attrib='FOOTER', margin=magrin)
    return page_df
