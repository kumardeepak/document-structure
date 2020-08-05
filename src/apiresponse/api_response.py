from apiresponse import status_codes as STATUS_CODES

switch = {
            STATUS_CODES.SUCCESS_GENERAL: {
                'message': 'api successful', 
                'http_code': 200
            },
            STATUS_CODES.SUCCESS_USER_REGISTERED: {
                'message': "user registered successfully", 
                'http_code': 200
            },
            STATUS_CODES.ERROR_USER_ALREADY_REGISTERED: {
                'message': 'user already exists, try using different username', 
                'http_code': 400
            },
            STATUS_CODES.SUCCESS_USER_LOGGED_IN: {
                'message': 'user logged-in successfully',
                'http_code': 200
            },
            STATUS_CODES.ERROR_USER_LOGIN: {
                'message': 'please check your login credentails and try again',
                'http_code': 400
            },
            STATUS_CODES.ERROR_LOGIN_FAILED_SYSTEM_ERROR: {
                'message': 'cannot proceed with user login, system error',
                'http_code': 500
            }
        }

def response(status_code, rsp):
        status = switch.get(status_code, {
                'message': 'processing failed because of unknown error, try reporting error to support@tarento.com', 
                'http_code': 200
            }
        )
        return {
            'status': {
                'code': status_code,
                'message': status['message']
            },
            'response': rsp
        }, status['http_code']
