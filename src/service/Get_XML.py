import os
from service.utilities import (extract_image_from_pdf, extract_xml_from_digital_pdf,
                       create_directory, read_directory_files, get_subdirectories,
                       get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered,
                       get_page_text_element_attrib, get_ngram
                      )
from service.xml_document_info import (get_xml_info)
from service.box_horizontal_operations import (merge_horizontal_blocks)
from service.box_vertical_operations import (merge_vertical_blocks)
from service.preprocess import  tag_heaader_footer_attrib

        
def xml_dfs(base_dir, filename):
    input_dir  = os.path.join(base_dir, 'input')
    output_dir = os.path.join('/home/ubuntu', '.output')
    os.system('mkdir -p {0}'.format(input_dir))
    os.system('mkdir -p {0}'.format(output_dir))

    pdf_filepath   = os.path.join(base_dir, filename)
    working_dir    = os.path.join(output_dir, os.path.splitext(filename)[0])

    ret            = create_directory(working_dir)

    pdf_image_dir  = extract_image_from_pdf(pdf_filepath, working_dir)
    pdf_xml_dir    = extract_xml_from_digital_pdf(pdf_filepath, working_dir)

    xml_files      = read_directory_files(pdf_xml_dir, pattern='*.xml')
    image_files    = read_directory_files(pdf_image_dir, pattern='*-*.jpg')
    xml_dfs, page_width, page_height = get_xml_info(xml_files[0])
    return xml_dfs, image_files, page_width, page_height
    
        
def get_vdf(xml_dfs,image_files,document_configs, file_index,header_region , footer_region):
    img_filepath   = image_files[file_index]
    df             = xml_dfs[file_index]
    in_df   = df.loc[:]
    in_df   = tag_heaader_footer_attrib(header_region , footer_region,in_df)

    h_df    = merge_horizontal_blocks(in_df, document_configs, debug=False)
    v_df    = merge_vertical_blocks(h_df, document_configs, debug=False)
    return v_df
