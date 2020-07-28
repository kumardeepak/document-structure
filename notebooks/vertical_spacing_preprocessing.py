import pandas as pd
import numpy as np
import os
from itertools import repeat

from xml_document_info import (get_xml_info)
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf, 
                        create_directory, read_directory_files, get_subdirectories,
                        get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib, get_ngram
                       )

def get_xml(input_dir,output_dir,filename):
	pdf_filepath   = os.path.join(input_dir, filename)
	working_dir    = os.path.join(output_dir, os.path.splitext(filename)[0])

	ret            = create_directory(working_dir)

	pdf_image_dir  = extract_image_from_pdf(pdf_filepath, working_dir)
	pdf_xml_dir    = extract_xml_from_digital_pdf(pdf_filepath, working_dir)

	xml_files      = read_directory_files(pdf_xml_dir, pattern='*.xml')


	image_files    = read_directory_files(pdf_image_dir, pattern='*-*.jpg')


	xml_dfs, page_width, page_height = get_xml_info(xml_files[0])
	return image_files,xml_dfs, page_width, page_height 


def append_dfs(dfs,width,height):
        page_no = []
        dataframe=pd.DataFrame()
        page_width = []
        page_height = []
        for num,df in enumerate(dfs):
            dataframe =dataframe.append(df)
            page_no.extend(repeat(num+1, len(df)))
            page_width.extend(repeat(width, len(df)))
            page_height.extend(repeat(height, len(df)))
        dataframe = dataframe.reset_index()
        dataframe["page_no"] = page_no
        dataframe["page_width"] = page_width
        dataframe["page_height"] = page_height
        return dataframe


def Drop_NullCol(dataframe):
	drop_col =[]
	for i,j in enumerate(dataframe['text']):
		if len(j.split())==0:
			drop_col.append(i)
	dataframe = dataframe.drop(dataframe.index[drop_col])
	dataframe = dataframe.reset_index()
	return dataframe

def verticle_spacing(dataframe):
    prev_spacing  = 0
    spacings = []
    for num in range(len(dataframe)):
        
        top = dataframe["text_top"][num]; height = dataframe["text_height"][num]   
        spacing      = top - prev_spacing
        prev_spacing = top + height
        spacings.append(spacing)
    dataframe["spacings"] = spacings

    dataframe = v_spacing(dataframe)

    return dataframe

def v_spacing(dataframe):
	prev_top=0
	prev_h=0
	prev_s=0
	prev_n=0
	spacing=[]
	for top,h,s,page_no in zip(dataframe['text_top'],dataframe['text_height'],dataframe['spacings'],dataframe['page_no']):
		s = top-prev_top-prev_h
    
		if s <0:
			if page_no!=prev_n:
				s=h
			else:
				s = prev_s
		spacing.append(s)
		prev_top = top
		prev_h=h
		prev_s=s
		prev_n=page_no
	dataframe['spacings']=spacing
	return dataframe

