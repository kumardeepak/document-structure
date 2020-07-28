import numpy as np
import pandas as pd
import glob
from collections import Counter
from itertools import repeat


def max_space_count(y):
    max_count = max(y,key=y.count)  
    count ={}
    avg=0
    for i in sorted(y)[:-1]:
        avg=avg+i
    avg_total = avg/len(y)
    for items,c in Counter(y).most_common():
        count[items]=c
    t=0; sort = sorted(count.items(), key=lambda x: x[1], reverse=True)
    if max_count<10:
        for i in sort:
            if i[0]>10:
                t=i[0]
                break
    else:
        t =max_count
    if t>=avg_total+15:
        return avg_total+15
    else:
        return t+6

def para_spacing_check(df,skip,length,threshold,paragraph,if_para,if_para_count):

    for line_num in range(length,length+len(df)):
        if skip >line_num:
            paragraph.append([left,top,right,bottom]),  if_para.append(if_para_count)
            continue
        spacing = int(df['spacings'][line_num]); left = int(df['text_left'][line_num]); right = int(df['text_width'][line_num]+left); top = int(df['text_top'][line_num]); bottom = int(df["text_height"][line_num]+top)

        last_line_flag =False
        if line_num+1<length+len(df):
            next_spacing = int(df['spacings'][line_num+1])
            if next_spacing<=threshold:
                skip = line_num+1;  spacing = next_spacing;  flag=False
                while spacing<=threshold:
                    left2 = int(df['text_left'][skip]); top2 = int(df['text_top'][skip]); bottom2 = int(df["text_height"][skip]+top2); right2 = int(df['text_width'][skip]+left2)
                    if skip+1==length+len(df):
                        flag=True
                        break
                    else:
                        skip =skip+1;   flag=True;   spacing = df['spacings'][skip]
                    if bottom2>bottom:
                        bottom = bottom2
                    if right2>right:
                        right = right2
                    if left2<left:
                        left = left2
                
                if flag and skip==length+len(df)-1:
                    if_para_count = if_para_count+1
                    last_line_flag  = True
                    left2 = int(df['text_left'][skip]); top2 = int(df['text_top'][skip]); bottom2 = int(df["text_height"][skip]+top2); right2 = int(df['text_width'][skip]+left2)
                    skip=skip+1
                    if bottom2>bottom:
                        bottom = bottom2
                    if right2>right:
                        right = right2
                    if left2<left:
                        left = left2

                    paragraph.append([left,top,right,bottom]); if_para.append(if_para_count)
                    
                elif flag and skip<length+len(df)-1:
                    if_para_count = if_para_count+1;  paragraph.append([left,top,right,bottom]); if_para.append(if_para_count)
                else:
                    if_para_count = if_para_count+1;  paragraph.append([left,top,right,bottom]); if_para.append(if_para_count)
            else:
                if_para_count = if_para_count+1;  paragraph.append([left,top,right,bottom]);  if_para.append(if_para_count)
        else:
            if_para_count = if_para_count+1;  paragraph.append([left,top,right,bottom]);   if_para.append(if_para_count)
            
    return paragraph,if_para,if_para_count 

def para_spacing(image_path,dfs):
    length=0
    page_num=0
    paragraph = []
    if_para  = []
    if_para_count=0
    for page_path in image_path:
        try:
            df = dfs[dfs["page_no"]==page_num+1];  skip = 0
            threshold = max_space_count(list(df["spacings"]))
            paragraph,if_para,if_para_count = para_spacing_check(df,skip,length,threshold,paragraph,if_para,if_para_count)
            page_num = page_num+1
            length = length+len(df)
        except:
            pass
        
    return paragraph,if_para       





def check_single_para(df,paragraph,if_para,if_para_count):
    
    total_para = sorted(np.unique(df["space_para_count"]));  skip =0
    for num,para_num in enumerate(total_para):
        if skip!=0:
            skip=skip-1
            continue
        para_df = df[df["space_para_count"]==para_num]; ind = df[df['space_para_count']==para_num].index.values.astype(int); left,top,right,bottom = para_df["space_paragraph"][ind[0]]
        length = len(para_df);  skip = 0
        
        if length==1 and num+1<len(total_para):
            next_para = df[df["space_para_count"]==total_para[num+1]]
            next_length = len(next_para)
            flag =False
            while next_length==1 and num+skip+1<len(total_para):
                next_para = df[df["space_para_count"]==total_para[num+skip+1]]; flag=True; ind = df[df['space_para_count']==total_para[num+skip+1]].index.values.astype(int)
                next_length = len(ind); left2,top2,right2,bottom2 = next_para["space_paragraph"][ind[0]];  length = length+next_length;  skip =skip +1
                if bottom2>bottom:
                    bottom = bottom2
                if left2<left:
                    left=left2
                if right2>right:
                    right =right2
            if flag:
                if_para_count = if_para_count+1
                paragraph.extend(repeat([left,top,right,bottom], length));   if_para.extend(repeat(if_para_count, length))
            else:
                if_para_count = if_para_count+1
                paragraph.extend(repeat([left,top,right,bottom], length));  if_para.extend(repeat(if_para_count, length))
        else:
            if_para_count = if_para_count+1
            paragraph.extend(repeat([left,top,right,bottom], length)); if_para.extend(repeat(if_para_count, length))
            
    return paragraph,if_para,if_para_count
    


def append_single_para(image_path,dfs):
    page_num=0
    paragraph = []
    if_para  = []
    if_para_count=0
    for page_path in image_path:
        
        df = dfs[dfs["page_no"]==page_num+1]
        paragraph,if_para,if_para_count = check_single_para(df,paragraph,if_para,if_para_count)
        page_num = page_num+1

    return paragraph,if_para       





def check_height(df,length,paragraph,if_para,if_para_count):
    
    total_para = sorted(np.unique(df["space_para_count_sentence"]))
    for para_num in total_para:
        para_df = df[df["space_para_count_sentence"]==para_num];ind = para_df[para_df['space_para_count_sentence']==para_num].index.values.astype(int)
        skip = 0
        for line_num in sorted(ind):
            if skip !=0:
                paragraph.append([left,top,right,bottom]); if_para.append(if_para_count)
                skip=skip-1
                continue
            height = int(para_df['text_height'][line_num]); left = int(para_df['text_left'][line_num]); right = int(para_df['text_width'][line_num]+left); top = int(para_df['text_top'][line_num])
            bottom = int(para_df["text_height"][line_num]+top)
            last_line_flag =False
            if line_num+1<=ind[-1]:
                next_height = int(para_df['text_height'][line_num+1]); times = line_num+1
                flag=False
                while (next_height==height and times<=ind[-1]) or ((next_height>height and next_height<height+2) and times<=ind[-1]) or ((next_height<height and next_height>height-2) and times<=ind[-1]):
                    
                    left2 = int(para_df['text_left'][times]); top2 = int(para_df['text_top'][times]); bottom2 = int(para_df["text_height"][times]+top2); right2 = int(para_df['text_width'][times]+left2)
                    times = times+1; bottom = bottom2; flag=True;  skip =skip+1 
                    if right2>right:
                        right = right2
                    if left2<left:
                        left = left2
                    if times>ind[-1]:
                        break
                    else:
                        next_height = para_df['text_height'][times]
                if flag and times-1==ind[-1]:
                    last_line_flag  = True
                    paragraph.append([left,top,right,bottom]);  if_para.append(if_para_count)
                elif flag and times-1<ind[-1]:
                    if_para_count = if_para_count+1
                    paragraph.append([left,top,right,bottom]);  if_para.append(if_para_count)
                else:
                    if_para_count = if_para_count+1
                    paragraph.append([left,top,right,bottom]);  if_para.append(if_para_count)
            else:
                if_para_count = if_para_count+1
                paragraph.append([left,top,right,bottom]);  if_para.append(if_para_count)
                
                
          
    return paragraph,if_para,if_para_count



def para_text_height(image_path,dfs):
    length=0
    page_num=0
    paragraph = []
    if_para  = []
    if_para_count=0
    for page_path1 in image_path:
        
        df = dfs[dfs["page_no"]==page_num+1]
        
        paragraph,if_para,if_para_count = check_height(df,length,paragraph,if_para,if_para_count)
        page_num = page_num+1
        length = length+len(df)

    return paragraph,if_para       
    


def update_para_no(dataframe,col_name):
    para_num = []
    para=0
    skip=0
    for num,i in enumerate(dataframe[col_name]):

        if skip!=0:
            para_num.append(para)
            skip=skip-1
            continue
        if num+1<len(dataframe):
            next_val=dataframe[col_name][num+1]
            next_num=num+1
            skip=0
            flag=False
            while next_val==i and next_num+1<len(dataframe):
                next_num=next_num+1
                next_val=dataframe[col_name][next_num]
                skip=skip+1
                flag=True

            if flag :
                para=para+1
                para_num.append(para)
            else:
                para=para+1
                para_num.append(para)
        else:
            if dataframe[col_name][num]==dataframe[col_name][num-1]:
                para_num.append(para)
            else:
                para_num.append(para+1) 
    return para_num
    
           

def get_iou(bb1, bb2):
    #assert bb1['x1'] < bb1['x2']
    #assert bb1['y1'] < bb1['y2']
    #assert bb2['x1'] < bb2['x2']
    #assert bb2['y1'] < bb2['y2']
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def check_iou(dataframe):
    total_para = np.unique(dataframe['height_para_no'])
    paragraph = [];  skip=0
    for i,para in enumerate(sorted(total_para)):
        if skip!=0:
            skip=skip-1
            continue
        df = dataframe[dataframe['height_para_no']==para];  ind = dataframe[dataframe['height_para_no']==para].index.values.astype(int)
        left,top,right,bottom = dataframe["height_paragraph"][ind[0]];  bb1 ={'x1':left,'y1':top,'x2':right,'y2':bottom};  total_length=len(df)
        if i+1<len(total_para):
            skip=0
            for para2 in  sorted(total_para)[i+1:]:
                df2 = dataframe[dataframe['height_para_no']==para2];  ind2 = dataframe[dataframe['height_para_no']==para2].index.values.astype(int)
                left2,top2,right2,bottom2  = dataframe["height_paragraph"][ind2[0]];  bb2 ={'x1':left2,'y1':top2,'x2':right2,'y2':bottom2}
                iou = get_iou(bb1,bb2)
                if iou*100>0.10:
                    total_length=total_length+len(df2)
                    skip=skip+1
                    if left2<left:
                        left=left2
                    if right2>right:
                        right=right2
                    if top2<top:
                        top=top2
                    if bottom2>bottom:
                        bottom=bottom2
                else:
                    break
            paragraph.extend(repeat([left,top,right,bottom], total_length))
        else:
            paragraph.extend(repeat([left,top,right,bottom], total_length))
    dataframe["paragraph"] = paragraph

    #Drop extra columns from dataframe
    dataframe = dataframe.drop(columns=["level_0","space_paragraph","space_para_count","space_paragraph_sentence","space_para_count_sentence","height_paragraph","height_para_count"])
    return dataframe
    





