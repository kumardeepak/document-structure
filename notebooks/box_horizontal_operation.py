import pandas as pd
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf, 
                        create_directory, read_directory_files, get_subdirectories,
                        get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib, get_ngram
                       )
from box_spacings_operation import (update_horizontal_spacings_v1, update_vertical_spacings_v1)
from box_conditions_evaluation import (are_vlines_too_close, are_vlines_close_enough,
                                       are_hlines_too_close, are_hlines_close_enough,
                                       are_hlines_aligned, are_lines_fonts_similar,
                                       arrange_grouped_line_indices, are_hlines_superscript,
                                       are_hlines)


def merge_hori_boxes(df, boxes, debug=False):
    t_ts       = []
    t_ls       = []
    t_ws       = []
    t_hs       = []
    texts      = []
    f_sizes    = []
    f_familys  = []
    f_colors   = []
    
    if debug:
        print('merge_hori_boxes: %s \n---------\n' % (str(boxes)))
        
    for box_item in boxes:
        line_indices, connection_type = box_item
        
        if connection_type == 'NOT_CONNECTED':
            for line_index in line_indices:
                t_ts.append(df.iloc[line_index]['text_top'])
                t_ls.append(df.iloc[line_index]['text_left'])
                t_hs.append(df.iloc[line_index]['text_height'])
                t_ws.append(df.iloc[line_index]['text_width'])
                texts.append(df.iloc[line_index]['text'])
                f_sizes.append(df.iloc[line_index]['font_size'])
                f_familys.append(df.iloc[line_index]['font_family'])
                f_colors.append(df.iloc[line_index]['font_color'])
        else:
            first_line_index = line_indices[0]
            last_line_index  = line_indices[-1]
            
            t_ts.append(df.iloc[first_line_index]['text_top'])
            t_ls.append(df.iloc[first_line_index]['text_left'])

            max_height = df.loc[first_line_index:last_line_index, 'text_height'].max()
            t_hs.append(max_height)

            t_ws.append(df.iloc[last_line_index]['text_left'] + df.iloc[last_line_index]['text_width'] - df.iloc[first_line_index]['text_left'])

            connected_text = ''
            for line_index in line_indices:
                connected_text = connected_text +  df.iloc[line_index]['text'] + ' '
            texts.append(connected_text)
            
            f_sizes.append(df.iloc[first_line_index]['font_size'])
            f_familys.append(df.iloc[first_line_index]['font_family'])
            f_colors.append(df.iloc[first_line_index]['font_color'])

    box_df = pd.DataFrame(list(zip(t_ts, t_ls, t_ws, t_hs, texts, 
                                   f_sizes, f_familys, f_colors)),
                          columns =['text_top', 'text_left', 'text_width', 'text_height', 'text', 
                                    'font_size', 'font_family', 'font_color'])
    
    box_df = update_horizontal_spacings_v1(box_df)
    box_df = update_vertical_spacings_v1(box_df)
    
    return box_df


def merge_hori_boxes_close(df, configs, debug=False):
    superscripts       = []
    new_df             = df.copy()
    new_df             = new_df.reset_index(drop=True)
    
    '''
       - normalize superscript case.
       - sub-script case is pending
       - multiple superscript in same line is pending
    '''
    index_grams = get_ngram(list(new_df.index.values), window_size=2)
    for index_gram in index_grams:
        is_superscript, idx1, idx2 = are_hlines_superscript(new_df, configs, index_gram[1], index_gram[0], debug=debug)
        if is_superscript:
            superscripts.append((idx1, idx2))
            
    if len(superscripts) > 0:
        for superscript in superscripts:
            new_df.at[superscript[1], 'text_height'] = df.iloc[superscript[0]]['text_height'] + abs(new_df.at[superscript[0], 'text_top'] - df.iloc[superscript[1]]['text_top'])
            new_df.at[superscript[0], 'text_top']    = df.iloc[superscript[1]]['text_top']
            
            new_df.at[superscript[1], 'font_size']   = df.iloc[superscript[0]]['font_size']
            new_df.at[superscript[1], 'font_family'] = df.iloc[superscript[0]]['font_family']
            new_df.at[superscript[1], 'font_color']  = df.iloc[superscript[0]]['font_color']

        new_df      = new_df.sort_values(by=['text_top', 'text_left'])
        new_df      = new_df.reset_index(drop=True)
    
    connections        = []
    index_grams        = get_ngram(list(new_df.index.values), window_size=2)
    for index_gram in index_grams:
        if are_hlines(new_df, configs, index_gram[0], index_gram[1], debug=debug) \
            and \
            are_lines_fonts_similar(new_df, configs, index_gram[0], index_gram[1], debug=debug) \
            and \
            (are_hlines_close_enough(new_df, configs, index_gram[0], index_gram[1], debug=debug) or \
                are_hlines_too_close(new_df, configs, index_gram[0], index_gram[1], debug=debug)) \
        :
            connections.append((index_gram[1], index_gram[0], 'CONNECTED'))
        else:
            connections.append((index_gram[1], index_gram[0], 'NOT_CONNECTED'))
    
    if debug:
        print("line connections (merge_hori_boxes_close) : %s \n----\n" % (str(connections)))
    
    grouped_lines = arrange_grouped_line_indices(connections, debug=debug)
    box_df        = merge_hori_boxes(new_df, grouped_lines, debug=debug)
    print('total records: %d, after merging records %d' % (new_df.shape[0], box_df.shape[0]))
    return box_df
