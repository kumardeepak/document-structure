import os
import pandas as pd
import Get_XML 
from left_right_on_block import left_right_margin
import config 


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

def main():
    Final_dfs = []
    xml_dfs, image_files = Get_XML.xml_dfs(config.base_dir, config.filename)
    Total_Page = len(xml_dfs)

    for file_index in range(Total_Page):
        v_df = Get_XML.get_vdf(xml_dfs, image_files,config.document_configs,file_index)
        p_df = process_page_blocks(v_df, config.document_configs,config.block_configs)
        p_df = p_df.reset_index()
        p_df = p_df.drop(columns=['level_0','index'])
        Final_dfs.append(p_df)


    return Final_dfs

