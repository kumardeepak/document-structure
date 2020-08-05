import logging
import os
import configs
from configs import development as dev_config

logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "server.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)

class AppConfig:
    @staticmethod
    def get_debug():
        return os.getenv("DEBUG", dev_config.DEBUG)
    
    @staticmethod
    def get_api_url_prefix():
        return "/api"

    @staticmethod
    def get_host():
        return os.getenv("APP_HOST", dev_config.APP_HOST)
    
    @staticmethod
    def get_port():
        return os.getenv("APP_PORT", dev_config.APP_PORT)

    @staticmethod
    def get_file_storage_path():
        return os.getenv("FILE_STORAGE_PATH", dev_config.FILE_STORAGE_PATH)
    
    @staticmethod
    def get_enable_cors():
        return os.getenv("ENABLE_CORS", dev_config.ENABLE_CORS)

    @staticmethod
    def get_jwt_secret_key():
        return os.getenv("JWT_SECRET_KEY", dev_config.JWT_SECRET_KEY)

    @staticmethod
    def get_jwt_access_token_expiry_in_mins():
        return os.getenv("JWT_ACCESS_TOKEN_EXPIRY_IN_MINS", dev_config.JWT_ACCESS_TOKEN_EXPIRY_IN_MINS)

    @staticmethod
    def get_jwt_refresh_token_expiry_in_days():
        return os.getenv("JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS", dev_config.JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS)

    @staticmethod
    def get_redis_hostname():
        return os.getenv("REDIS_HOSTNAME", dev_config.REDIS_HOSTNAME)

    @staticmethod
    def get_redis_port():
        return os.getenv("REDIS_PORT", dev_config.REDIS_PORT)

    @staticmethod
    def get_supported_upload_file_types():
        return os.getenv("SUPPORTED_UPLOAD_FILETYPES", dev_config.SUPPORTED_UPLOAD_FILETYPES)
