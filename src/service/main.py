import os
import pandas as pd
from service import Get_XML
from service.left_right_on_block import left_right_margin
from  configs import config
from service.preprocess import prepocess_pdf_rgions

def process_page_blocks(page_df, configs,block_configs, debug=False):
    cols      = page_df.columns.values.tolist()
    
    df        = pd.DataFrame(columns=cols)
    
    block_index = 0
    for index, row in page_df.iterrows():
        if row['children'] == None:
            df = df.append(page_df.iloc[index])
        else:
            dfs = process_block(page_df.iloc[index], block_configs)
            df = df.append(dfs)
    return df


def process_block(children, block_configs):
    
    dfs = left_right_margin(children, block_configs)
    return dfs

def get_response(p_df,img_df,page_no,page_width,page_height):

    p_df['block_id'] = range(len(p_df))
    myDict = {'page_no': page_no,'page_width': page_width,'page_height':page_height,'image':{},'blocks':{}}
    image_data = process_image_df(myDict,img_df)
    myDict['image']=image_data
    page_data = df_to_json(p_df)
    myDict['blocks']=page_data
    return myDict


def df_to_json(p_df):
    page_data = []
    p_df  = p_df.where(p_df.notnull(), None)
    if len(p_df) > 0 :
        
        drop_col = ['index', 'xml_index','level_0']  
        for col in drop_col:
            if col in p_df.columns:
                p_df=p_df.drop(columns=[col])

        for index ,row in p_df.iterrows():
            block = row.to_dict()
            for key in block.keys():
                if key not in ['text', 'children']:
                    try :
                        block[key] = int(block[key])
                    except :
                        pass
            if 'children' in list(block.keys()):
                if block['children'] == None :
                    pass
                else :
                    block['text'] = None
                    block['children'] = df_to_json(pd.read_json(row['children']))
            page_data.append(block)
        
    return page_data

def process_image_df(myDict,img_df):
    image_data = []
    if len(img_df)>0:
        drop_col = ['index', 'xml_index','level_0']  
        for col in drop_col:
            if col in img_df.columns:
                img_df=img_df.drop(columns=[col])
                
        for index ,row in img_df.iterrows():
            block = row.to_dict()
            image_data.append(block)
        return image_data
    else:
        return None
    
def DocumentStructure(file_name):
    
    img_dfs,xml_dfs, image_files, page_width, page_height = Get_XML.xml_dfs(config.base_dir, file_name)
    multiple_pages = False
    if len(xml_dfs) > 1:
        multiple_pages =True
    header_region, footer_region = prepocess_pdf_rgions(xml_dfs, page_height)



    Total_Page = len(xml_dfs)
    response = {'result':[]}
    for file_index in range(Total_Page):
        img_df = img_dfs[file_index]
        v_df = Get_XML.get_vdf(xml_dfs, image_files,config.document_configs,file_index,header_region , footer_region,multiple_pages)
        p_df = process_page_blocks(v_df, config.document_configs,config.block_configs)
        p_df = p_df.reset_index(drop=True)
        final_json = get_response(p_df,img_df,file_index,page_width,page_height)
        response['result'].append(final_json)

    return response


