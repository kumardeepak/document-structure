from flask_restful import fields, marshal_with, reqparse, Resource
from flask_jwt_extended import (jwt_required,create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import werkzeug
from flask import send_file
import os
import logging
import uuid
import magic
from configs import AppConfig

ALLOWED_FILE_TYPES  = AppConfig.get_supported_upload_file_types()
parser              = reqparse.RequestParser(bundle_errors=True)

class FileUploadResource(Resource):
    @jwt_required
    def post(self):
        parse       = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', help='File is required', required=True)
        args        = parse.parse_args()
        f           = args['file']
        filename    = str(uuid.uuid4())+'_'+f.filename
        filepath    = os.path.join(AppConfig.get_file_storage_path(), filename)
        f.save(filepath)
        with open(filepath, 'rb') as f:
            filetype = magic.from_buffer(f.read(), mime=True)
            f.close()
            if filetype in ALLOWED_FILE_TYPES:
                return {
                    'status': {
                        'code': 200,
                        'message': 'api successful'
                    },
                    'rsp' : {
                        'filename': filename
                    }
                }
            else:
                f.close()
                os.remove(filepath)
                return {
                    'status': {
                        'code': 400,
                        'message': 'unsupported file type'
                    }
                }, 400
        

class FileDownloadResource(Resource):
    def get(self):
        parse       = reqparse.RequestParser()
        parse.add_argument('filename', type=str, location='args', help='Filename is required', required=True)
        args        = parse.parse_args()
        filename    = args['filename']
        filepath    = os.path.join(AppConfig.get_file_storage_path(), filename)
        if(os.path.exists(filepath)):
            result  = send_file(filepath, as_attachment=True)
            result.headers["x-suggested-filename"] = filename
            return result
        else:
            return {
                    'status': {
                        'code': 400,
                        'message': 'file not found'
                    }
                }, 400