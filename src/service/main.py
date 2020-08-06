import os
import pandas as pd
from service import Get_XML
from service.left_right_on_block import left_right_margin
from  configs import config


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

def get_response(p_df,page_no,page_width,page_height):

    p_df['block_id'] = range(len(p_df))
    myDict = {'page_no': page_no,'page_width': page_width,'page_height':page_height,'blocks':{}}
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
def DocumentStructure(file_name):
    
    xml_dfs, image_files, page_width, page_height = Get_XML.xml_dfs(config.base_dir, file_name)
    Total_Page = len(xml_dfs)
    response = {'result':[]}
    for file_index in range(Total_Page):
        v_df = Get_XML.get_vdf(xml_dfs, image_files,config.document_configs,file_index)
        p_df = process_page_blocks(v_df, config.document_configs,config.block_configs)
        p_df = p_df.reset_index()
        final_json = get_response(p_df, file_index,page_width,page_height)
        response['result'].append(final_json)

    return response


