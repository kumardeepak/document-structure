
#base_dir   = '/home/naresh/Tesseract/DS_Module/data/input/'
#base_dir   = '/home/dhiraj/Documents/Anuwad/document-structure/data/input'
base_dir = '/opt/share/nginx/upload'
filename   = '6251_2016_3_1501_19387_Judgement_06-Jan-2020.pdf'
HOST = '0.0.0.0'
PORT = 7000

# logging.basicConfig(
#     filename=os.getenv("SERVICE_LOG", "server.log"),
#     level=logging.DEBUG,
#     format="%(levelname)s: %(asctime)s \
#         pid:%(process)s module:%(module)s %(message)s",
#     datefmt="%d/%m/%y %H:%M:%S",
# )

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

preprocess_config = {'header_cut':0.15  , 'footer_cut' :0.15 ,'repeat_threshold' :0.95}