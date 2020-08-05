import os
from utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf,
                       create_directory, read_directory_files, get_subdirectories,
                       get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib, get_ngram
                      )
from xml_document_info import (get_xml_info)
from box_horizontal_operations import (merge_horizontal_blocks)
from box_vertical_operations import (merge_vertical_blocks)

        
def process(base_dir, filename, document_configs, file_index):
    input_dir  = os.path.join(base_dir, 'input')
    output_dir = os.path.join(base_dir, 'output')
    pdf_filepath   = os.path.join(input_dir, filename)
    working_dir    = os.path.join(output_dir, os.path.splitext(filename)[0])

    ret            = create_directory(working_dir)

    pdf_image_dir  = extract_image_from_pdf(pdf_filepath, working_dir)
    pdf_xml_dir    = extract_xml_from_digital_pdf(pdf_filepath, working_dir)

    xml_files      = read_directory_files(pdf_xml_dir, pattern='*.xml')
    image_files    = read_directory_files(pdf_image_dir, pattern='*-*.jpg')
    xml_dfs, page_width, page_height = get_xml_info(xml_files[0])
    img_filepath   = image_files[file_index]
    df             = xml_dfs[file_index]
    in_df   = df.loc[:]

    h_df    = merge_horizontal_blocks(in_df, document_configs, debug=False)
    v_df    = merge_vertical_blocks(h_df, document_configs, debug=False)
    return v_df
        
        
