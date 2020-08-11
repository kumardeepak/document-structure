DEBUG                                   = True
API_URL_PREFIX                          = "/api"
APP_HOST                                = '0.0.0.0'
APP_PORT                                = 7000
FILE_STORAGE_PATH                       = '/Users/kd/Workspace/python/face/data/input' #'/tmp/nginx'
BASE_DIR                                = '/opt/share/nginx/upload'
FILE_NAME                                = '6251_2016_3_1501_19387_Judgement_06-Jan-2020.pdf'
ENABLE_CORS                             = True

JWT_SECRET_KEY                          = 'tarento@ai.com$'
JWT_ACCESS_TOKEN_EXPIRY_IN_MINS         = 5
JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS        = 30
REDIS_HOSTNAME                          = 'localhost'
REDIS_PORT                              = 6379

SUPPORTED_UPLOAD_FILETYPES              = ['application/msword',
'application/pdf',
'image/x-ms-bmp',
'image/jpeg',
'image/jpg',
'image/png',
'text/plain',
'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'video/mp4',
'video/webm']



DOCUMENT_CONFIGS = {
    'LANGUAGE_TYPE': 'eng',
    
    'HORI_BLOCK_WDTH_DIFF_PERC': 0.85,
    'SUPERSCRIPT_HEIGHT_DIFFERENCE': 7.0,
    'HORI_SPACE_TOO_CLOSE': 10.0,
    
    'VERTICAL_SPACE_TOO_CLOSE': 5.0,
    'AVERAGE_VERTICAL_SPACE': 12.0,
    'LEFT_OR_RIGHT_ALIGNMENT_MARGIN': 20.0
}

BLOCK_CONFIGS = {
    "right_margin_threshold": 0.10,  "left_margin_threshold": 0.10,
    "right_break_threshold": 0.04,   "left_break_threshold": 0.05,
    "header_left_threshold": 0.70,  "header_right_threshold": 0.85,
    "space_multiply_factor": 1.8
}

PREPROCESS_CONFIGS = {'header_cut':0.15  , 'footer_cut' :0.15 ,'repeat_threshold' :0.95}
