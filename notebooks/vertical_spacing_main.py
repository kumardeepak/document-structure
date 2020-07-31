import os
import glob
import vertical_spacing_packages
import vertical_spacing_preprocessing
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
#from box_spacings_operation import (update_horizontal_spacings_v1, update_vertical_spacings_v1)

from box_horizontal_operations import (merge_horizontal_blocks)


def main(image_files,xml_dfs, page_width, page_height,document_configs):
	hproc_dfs = []
	for df in xml_dfs:
	    dfs = merge_horizontal_blocks(df, document_configs, debug=False)
	    hproc_dfs.append(dfs)

	#### PREPROCESSING TO APPEND ALL DATAFRAMES , REMOVE NULL ROWS, AND CREATE VERTICLE SPACING COLUMN
	dataframe = vertical_spacing_preprocessing.append_dfs(hproc_dfs,page_width,page_height)
	dataframe =  vertical_spacing_preprocessing.Drop_NullCol(dataframe)
	dataframe =  vertical_spacing_preprocessing.verticle_spacing(dataframe)
	#print(dataframe)

	#### PARAGRAPH CREATION BASED ON VERTICLE SPACINGS
	#print(len(dataframe))
	#print(image_files)
	paragraph,if_para = vertical_spacing_packages.para_spacing(image_files,dataframe)
	dataframe["space_paragraph"] = paragraph
	dataframe["space_para_count"] = if_para

	#### APPEND SINGLE PARAGRAPH TO AVOID FROM BREKDOWN OF SINGLE PARAGRAPH
	paragraph,if_para = vertical_spacing_packages.append_single_para(image_files,dataframe)
	dataframe["space_paragraph_sentence"]=paragraph
	dataframe["space_para_count_sentence"]=if_para

	#### PARAGRAPH CREATION BASED ON TEXT HEIGHT
	paragraph,if_para = vertical_spacing_packages.para_text_height(image_files,dataframe)
	dataframe["height_paragraph"]=paragraph
	dataframe["height_para_count"]=if_para


	para_num = vertical_spacing_packages.update_para_no(dataframe,'height_paragraph')
	dataframe["height_para_no"] = para_num

	#### REMOVE OVERLAPPING PARAGRAPH BASED ON IOU
	dataframe = vertical_spacing_packages.check_iou(dataframe)
	para_num = vertical_spacing_packages.update_para_no(dataframe,'height_para_no')
	dataframe["para_no"] = para_num
	dataframe = dataframe.drop(columns=["height_para_no"])
	return dataframe

#### DRAW PARAGRAPH BOUNDING BOX IN IMAGES
def draw_bbox_coord(image_path,dfs):
    page_num=0
    for filepath in image_path:
        try:
            save_filepath = os.path.join(os.path.dirname(filepath), 'result_' + os.path.basename(filepath))
            df = dfs[dfs["page_no"]==page_num+1]
            ind = dfs[dfs["page_no"]==page_num+1].index.values.astype(int)
            image  = Image.open(filepath)
            page_w = int(df['page_width'][ind[0]+1])
            page_h = int(df['page_height'][ind[0]+1])
            image = image.resize((page_w,page_h))
            draw   = ImageDraw.Draw(image)
            for i in df["paragraph"]:
                left,top,right,bottom = i
                draw.rectangle(((left,top), (right,bottom)), outline="green")
            image.save(save_filepath)
            
        except:
            pass
        page_num = page_num+1
    #return image        
    

#image = draw_bbox_coord(image_files,dataframe)
#print("done")


