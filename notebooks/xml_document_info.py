import pandas as pd
import os
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf, 
                        create_directory, read_directory_files, get_subdirectories,
                        get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib
                       )

def get_document_width_height(pages):
    return int(pages[0].attrib['width']), int(pages[0].attrib['height'])

'''
    -    Normalizes the left & width value currently
'''
def normalize_page_xml_df(in_df, width, height):
    df = in_df.copy(deep=True)
    
    for index, row in df.iterrows():
        if row['text_left'] < 0:
            df.at[index, 'text_left'] = abs(in_df.iloc[index]['text_left'])
            
        if row['text_left'] + row['text_width'] > width:
            df.at[index, 'text_width'] = in_df.iloc[index-1]['text_width']
    
    return df

'''
    - Remove all range of rows between
        - 'Digitally signed by' & 'Signature Not Verified'. This is primarily meant for SC judgment
'''
def remove_redundant_rows(in_df):
    df          = in_df.copy(deep=True)
    start_index = 0
    end_index   = 0
    
    start       = df.index[df['text'] == 'Digitally signed by'].tolist()
    if (len(start) > 0):
        start_index = start[0]

    end   = df.index[df['text'] == 'Signature Not Verified'].tolist()
    if (len(end) > 0):
        end_index = end[0]
    
    indices = []
    if (start_index != 0 and end_index != 0) and (start_index < end_index):
        for i in range(start_index, end_index+1):
            indices.append(df.index[i])
        df = df.drop(indices)
    
    return df

def get_xml_info(filepath):
    xml             = get_xmltree(filepath)
    tag             = 'page'
    pages           = get_specific_tags(xml, tag)
    print('Total number of pages (%d) in file (%s)' % (len(pages), os.path.basename(filepath)))
    
    width, height   = get_document_width_height(pages)
    fonts           = get_specific_tags(xml, 'fontspec')

    dfs             = []
    for page in pages:
        t_ts        = []
        t_ls        = []
        t_ws        = []
        t_hs        = []
        f_sizes     = []
        f_familys   = []
        f_colors    = []
        ts          = []
        
        texts       = get_specific_tags(page, 'text')
        
        for index, text in enumerate(texts):
            p_t, p_l, p_w, p_h, t_t, t_l, t_w, t_h, f_size, f_family, f_color, t = get_page_text_element_attrib(fonts, page, text)
            if len(t.strip()) < 1:
                continue

            t_ts.append(t_t)
            t_ls.append(t_l)
            t_ws.append(t_w)
            t_hs.append(t_h)
            f_sizes.append(f_size)
            f_familys.append(f_family)
            f_colors.append(f_color)
            ts.append(t)
        
        df = pd.DataFrame(list(zip(t_ts, t_ls, t_ws, t_hs,
                                        ts, f_sizes, f_familys, f_colors)), 
                          columns =['text_top', 'text_left', 'text_width', 'text_height',
                                      'text', 'font_size', 'font_family', 'font_color'])
        '''
            remove rows that are redundant.
        '''
        df  = remove_redundant_rows(df)

        df.sort_values(by=['text_top'],inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'xml_index'},inplace=True)
        dfs.append(normalize_page_xml_df(df, width, height))

    return dfs, width, height

