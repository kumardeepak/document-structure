import pandas as pd
import os
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf, 
                        create_directory, read_directory_files, get_subdirectories,
                        get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib
                       )

def get_document_width_height(pages):
    return int(pages[0].attrib['width']), int(pages[0].attrib['height'])

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
            right_empty_space = 4 * (len(t) - len(t.rstrip()) + 1)
            left_empty_space  = 4 * (len(t) - len(t.lstrip()))

            if len(t.strip()) < 1:
                continue

            t_ts.append(t_t)
            '''
                outlier condition. text_left has been reported to negative.
                                        - currently we have made it +ve value.
                                    text_width sometimes crosses page width. In order to handle it
                                        - count empty space and multiply by factor 4. Ideally it is dependent upon font size.
                                        - also ignoring left_empty_space
            '''
            
            t_ls.append(abs(t_l))

            if (t_w + t_l) > width:
                t_w1 = (t_w - right_empty_space)
                t_ws.append(t_w1)
            else:
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
        df.sort_values(by=['text_top'],inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'xml_index'},inplace=True)
        #print(df.head())
    
        dfs.append(df)

    return dfs, width, height
