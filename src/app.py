import redis
from datetime import timedelta
from flask import Flask, jsonify
from flask.blueprints import Blueprint
from flask_cors import CORS
from configs import config

# from flask_jwt_extended import (
#     JWTManager, create_access_token, create_refresh_token, get_jti,
#     jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
# )

import routes
import logging
import os
from configs.backup_config import AppConfig


server                                          = Flask(__name__)
# server.config['JWT_SECRET_KEY']                 = AppConfig.get_jwt_secret_key()
# server.config['PROPAGATE_EXCEPTIONS']           = True
# server.config['JWT_ACCESS_TOKEN_EXPIRES']       = timedelta(minutes=AppConfig.get_jwt_access_token_expiry_in_mins())
# server.config['JWT_REFRESH_TOKEN_EXPIRES']      = timedelta(days=AppConfig.get_jwt_refresh_token_expiry_in_days())
# server.config['JWT_BLACKLIST_ENABLED']          = True
# server.config['JWT_BLACKLIST_TOKEN_CHECKS']     = ['access', 'refresh']
#
# jwt                                             = JWTManager(server)

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint)#, url_prefix=AppConfig.get_api_url_prefix())

#@server.route('/api/v1/info', methods=['GET'])
if __name__ == "__main__":
    print(server.url_map)
    #server.run(host=config.HOST, port=config.PORT, debug=False)
    server.run(host=AppConfig.get_host(), port=AppConfig.get_port(), debug=AppConfig.get_debug())
