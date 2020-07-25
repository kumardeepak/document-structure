import pandas as pd
from itertools import groupby

def arrange_grouped_line_indices(line_connections, debug=False):
    lines          = [list(i) for j, i in groupby(line_connections, lambda a: a[2])]
    if debug:
        print('arrange_grouped_line_indices: %s \n---------\n' % (str(lines)))
        
    arranged_lines = []

    for line_items in lines:
        indices = []
        for line_item in line_items:
            indices.append(line_item[0])
            indices.append(line_item[1])
        indices = sorted(list(set(indices)))
        arranged_lines.append([indices, line_items[0][2]])
        
    if debug:
        print('arrange_grouped_line_indices,arranged_lines : %s \n---------\n' % (str(arranged_lines)))
    
    final_arranged_lines = []
    
    if len(arranged_lines) == 1:
        final_arranged_lines.append([arranged_lines[0][0], arranged_lines[0][1]])
    else:
        for index, line_item in enumerate(arranged_lines):
            if index == 0 and line_item[1] == 'NOT_CONNECTED':
                del line_item[0][-1]
            if index > 0 and index < (len(arranged_lines) - 1) and line_item[1] == 'NOT_CONNECTED':
                del line_item[0][0]
                del line_item[0][-1]
            if index == (len(arranged_lines) - 1) and line_item[1] == 'NOT_CONNECTED':
                del line_item[0][0]

            final_arranged_lines.append([line_item[0], line_item[1]])
            
    return final_arranged_lines


def are_lines_fonts_similar(df, configs, idx1, idx2, debug=False):
    if (abs(df.iloc[idx1]['font_size'] - df.iloc[idx2]['font_size']) < 2.0) \
            and (df.iloc[idx1]['font_family'] == df.iloc[idx2]['font_family']):
        return True
    return False

def are_hlines_aligned(df, configs, idx1, idx2, debug=False):
    line1_left = df.iloc[idx1]['text_left']
    line2_left = df.iloc[idx2]['text_left']
    line1_right = df.iloc[idx1]['text_left'] + df.iloc[idx1]['text_width']
    line2_right = df.iloc[idx2]['text_left'] + df.iloc[idx2]['text_width']
    
    if (abs(line2_left - line1_left) < configs['LEFT_OR_RIGHT_ALIGNMENT_MARGIN']) and \
        (abs(line2_right - line1_right) < configs['LEFT_OR_RIGHT_ALIGNMENT_MARGIN']):
        return True
    return False

def get_lines_upper_lower(df, idx1, idx2):
    if df.iloc[idx2]['text_top'] > df.iloc[idx1]['text_top']:
        return idx1, idx2
    return idx2, idx1

def are_vlines(df, configs, idx1, idx2, debug=False):
    first_idx, sec_idx  = get_lines_upper_lower(df, idx1, idx2)
    space               = df.iloc[sec_idx]['text_top'] - (df.iloc[first_idx]['text_top'] + df.iloc[first_idx]['text_height'])
    if space > configs['VERTICAL_SPACE_TOO_CLOSE']:
        return True
    return False


def are_vlines_close_enough(df, configs, idx1, idx2, debug=False):
    space = ((df.iloc[idx1]['text_top'] + df.iloc[idx1]['text_height'])) - df.iloc[idx2]['text_top']
    if debug:
        print('are_vlines_close_enough:: idx1: %d, idx2: %d, space: %d' % (idx1, idx2, space))
    if space < configs['AVERAGE_VERTICAL_SPACE']:
        return True
    return False

def are_vlines_too_close(df, configs, idx1, idx2, debug=False):
    first_idx, sec_idx  = get_lines_upper_lower(df, idx1, idx2)
    space               = df.iloc[sec_idx]['text_top'] - (df.iloc[first_idx]['text_top'] + df.iloc[first_idx]['text_height'])

    if debug:
        print('are_vlines_too_close:: idx1: %d, idx2: %d, space: %d' % (idx1, idx2, space))
    if space <= configs['VERTICAL_SPACE_TOO_CLOSE']:
        return True
    return False

def are_vlines_zero_overlap(df, configs, idx1, idx2, debug=False):
    first_idx, sec_idx  = get_lines_upper_lower(df, idx1, idx2)
    if (df.iloc[first_idx]['text_left'] > df.iloc[sec_idx]['text_left']):
        if (df.iloc[sec_idx]['text_left'] + df.iloc[sec_idx]['text_width']) < df.iloc[first_idx]['text_left']:
            return True, abs((df.iloc[sec_idx]['text_left'] + df.iloc[sec_idx]['text_width']) - df.iloc[first_idx]['text_left'])
    else:
        if (df.iloc[first_idx]['text_left'] + df.iloc[first_idx]['text_width']) < df.iloc[sec_idx]['text_left']:
            return True, abs((df.iloc[first_idx]['text_left'] + df.iloc[first_idx]['text_width']) - df.iloc[sec_idx]['text_left'])
    return False, 0.0

def are_vlines_full_overlap(df, configs, idx1, idx2, debug=False):
    first_idx, sec_idx  = get_lines_upper_lower(df, idx1, idx2)
    if (df.iloc[first_idx]['text_left'] > df.iloc[sec_idx]['text_left']):
        if (df.iloc[sec_idx]['text_left'] + df.iloc[sec_idx]['text_width']) < (df.iloc[first_idx]['text_left'] + df.iloc[first_idx]['text_width']):
            return True, (abs(df.iloc[sec_idx]['text_width'] - df.iloc[first_idx]['text_width']))
    else:
        if (df.iloc[first_idx]['text_left'] + df.iloc[first_idx]['text_width']) > (df.iloc[sec_idx]['text_left'] + df.iloc[sec_idx]['text_width']):
            return True, (abs(df.iloc[sec_idx]['text_width'] - df.iloc[first_idx]['text_width']))
    return False, 0.0

def are_vlines_partial_overlap(df, configs, idx1, idx2, debug=False):
    first_idx, sec_idx  = get_lines_upper_lower(df, idx1, idx2)

def are_hlines_too_close(df, configs, idx1, idx2, debug=False):
    space = abs((df.iloc[idx1]['text_left'] + df.iloc[idx1]['text_width']) - df.iloc[idx2]['text_left'])
    if debug:
        print('are_hlines_too_close:: idx1: %d, idx2: %d, space: %d' % (idx1, idx2, space))
    if space <= configs['HORI_SPACE_TOO_CLOSE']:
        return True
    return False

def are_hlines_superscript(df, configs, idx1, idx2, debug=False):

    if (abs(df.iloc[idx1]['text_top'] - df.iloc[idx2]['text_top']) <= configs['SUPERSCRIPT_HEIGHT_DIFFERENCE']):
        if df.iloc[idx1]['text_left'] < df.iloc[idx2]['text_left']:
            if df.iloc[idx1]['text_height'] < df.iloc[idx2]['text_height']:
                return True, idx1, idx2
        else:
            if df.iloc[idx1]['text_height'] < df.iloc[idx2]['text_height']:
                return True, idx2, idx1
    
    return False, idx1, idx2

def are_hlines_close_enough(df, configs, idx1, idx2, debug=False):
    if (abs(df.iloc[idx1]['text_width'] - df.iloc[idx2]['text_width']) / (max(df.iloc[idx1]['text_width'], df.iloc[idx2]['text_width'])) \
            > configs['HORI_BLOCK_WDTH_DIFF_PERC'] ):
        return True
    return False

def are_hlines(df, configs, idx1, idx2, debug=False):
    space = abs(df.iloc[idx1]['text_top'] - df.iloc[idx2]['text_top'])
    if debug:
        print('are_hlines:: idx1: %d, idx2: %d, space: %d' % (idx1, idx2, space))
    return space <= configs['SUPERSCRIPT_HEIGHT_DIFFERENCE']