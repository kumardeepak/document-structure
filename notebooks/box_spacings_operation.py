import pandas as pd

def update_horizontal_spacings_v1(df):
    horizontal_spacings     = []
    prev_top                = 0

    for index in range(df.shape[0]):
        curr_top = df.iloc[index]['text_top']
        if  curr_top > prev_top:
            horizontal_space    = 0
            prev_top            = curr_top
        else:
            horizontal_space    = df.iloc[index]['text_left'] \
                                    - (df.iloc[index-1]['text_left'] + df.iloc[index-1]['text_width'])
        horizontal_spacings.append(horizontal_space)

    new_df = df.copy()
    if 'horizontal_space' in new_df.columns:
        del new_df['horizontal_space']
    new_df['horizontal_space'] = horizontal_spacings
    return new_df


def update_vertical_spacings_v1(df):
    vertical_spacings       = []
    prev_top                = 0
    prev_height             = 0
    prev_vertical_space     = 0

    for index in range(df.shape[0]):
        curr_top    = df.iloc[index]['text_top']
        curr_height = df.iloc[index]['text_height']
        if  curr_top > prev_top:
            vertical_space      = curr_top - (prev_top+prev_height)
            
            prev_top            = curr_top
            prev_height         = curr_height
            prev_vertical_space = vertical_space
        else:
            vertical_space      = prev_vertical_space
        
        if index == 0:
            vertical_space      = 0
        vertical_spacings.append(vertical_space)
    
    new_df = df.copy()
    if 'vertical_space' in new_df.columns:
        del new_df['vertical_space']
    new_df['vertical_space'] = vertical_spacings
    return new_df