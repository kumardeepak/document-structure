from flask import Blueprint
from flask_restful import Api
from resources.fileupload  import FileUploadResource, FileDownloadResource

FILEUPLOAD_BLUEPRINT      = Blueprint("fileupload", __name__)

Api(FILEUPLOAD_BLUEPRINT).add_resource(FileUploadResource,        "/v1/file/upload")
Api(FILEUPLOAD_BLUEPRINT).add_resource(FileDownloadResource,      "/v1/file/download")
