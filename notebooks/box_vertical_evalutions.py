import pandas as pd

def are_vlines(df, configs, idx1, idx2, debug=False):
    space = abs(df.iloc[idx1]['text_top'] - df.iloc[idx2]['text_top'])
    if debug:
        print('are_hlines:: idx1: %d, idx2: %d, space: %d' % (idx1, idx2, space))
    return space <= configs['SUPERSCRIPT_HEIGHT_DIFFERENCE']
