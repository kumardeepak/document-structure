import pandas as pd
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf, create_directory, read_directory_files, get_subdirectories,
                        get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered, get_page_text_element_attrib, get_ngram)

from box_horizontal_evalutions import (are_hlines)
from box_grouping import arrange_grouped_line_indices

def merge_horizontal_blocks(in_df, configs, debug=False):
    df                 = in_df.copy(deep=True)
    df                 = in_df.reset_index(drop=True)
    
    connections        = []
    index_grams        = get_ngram(list(df.index.values), window_size=2)
    
    for index_gram in index_grams:
        if are_hlines(df, configs, index_gram[0], index_gram[1], debug=debug):
            connections.append((index_gram[1], index_gram[0], 'CONNECTED'))
        else:
            connections.append((index_gram[1], index_gram[0], 'NOT_CONNECTED'))

    if debug:
        print("block connections (get_document_horizontal_blocks) : %s \n----\n" % (str(connections)))
        
    grouped_lines   = arrange_grouped_line_indices(connections, debug=debug)
    cols            = df.columns.values.tolist()
    cols.append('children')
    block_df        = pd.DataFrame(columns=cols)

    index     = 0
    for lines in grouped_lines:
        line_indices, connection_type = lines
        if connection_type == 'NOT_CONNECTED':
            for line_index in line_indices:
                block_df.loc[index] = df.iloc[line_index]
                block_df.loc[index]['children'] = None
                index += 1
        else:
            children_df  = df.loc[lines[0][0]:lines[0][-1]].copy(deep=True)
            
            top          = children_df['text_top'].min()
            left         = children_df['text_left'].min()
            width        = children_df[['text_left', 'text_width']].sum(axis=1).max() - left
            
            children_df.sort_values('text_top', axis = 0, ascending = True, inplace=True)
            height       =  (children_df.iloc[-1]['text_top'] + children_df.iloc[-1]['text_height']) - children_df['text_top'].min()
            
            block_df.at[index, 'text_top']     = top
            block_df.at[index, 'text_left']    = left
            block_df.at[index, 'text_height']  = height
            block_df.at[index, 'text_width']   = width
            
            block_df.at[index, 'text']         = ' '.join(children_df['text'].values.tolist())

            block_df.at[index, 'xml_index']    = children_df['xml_index'].min()

            children_df.sort_values('text_width', axis = 0, ascending = True, inplace=True)

            block_df.at[index, 'font_size']    = children_df.iloc[-1]['font_size']
            block_df.at[index, 'font_family']  = children_df.iloc[-1]['font_family']
            block_df.at[index, 'font_color']   = children_df.iloc[-1]['font_color']
            block_df.at[index, 'children']     = children_df.to_json()
            index += 1
    
    return block_df