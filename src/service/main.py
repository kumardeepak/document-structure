import os
import pandas as pd
from Get_XML import process
from left_right_on_block import left_right_margin



base_dir   = '/home/naresh/Tesseract/DS_Module/data'
filename   = '6251_2016_3_1501_19387_Judgement_06-Jan-2020.pdf'


document_configs = {
    'LANGUAGE_TYPE': 'eng',
    
    'HORI_BLOCK_WDTH_DIFF_PERC': 0.85,
    'SUPERSCRIPT_HEIGHT_DIFFERENCE': 7.0,
    'HORI_SPACE_TOO_CLOSE': 10.0,
    
    'VERTICAL_SPACE_TOO_CLOSE': 5.0,
    'AVERAGE_VERTICAL_SPACE': 12.0,
    'LEFT_OR_RIGHT_ALIGNMENT_MARGIN': 20.0
}

block_configs = {
    "right_margin_threshold": 0.10,  "left_margin_threshold": 0.10,
    "right_break_threshold": 0.04,   "left_break_threshold": 0.05,
    "header_left_threshold": 0.70,  "header_right_threshold": 0.85,
    "space_multiply_factor": 1.8
}

file_index=2
v_df = process(base_dir, filename, document_configs, file_index)


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


p_df = process_page_blocks(v_df, document_configs,block_configs)
p_df = p_df.reset_index()
p_df = p_df.drop(columns=['level_0','index'])

print(p_df)
