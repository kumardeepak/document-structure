import json
from datetime import datetime

class UserServiceProvider:
    def __init__(self, args):
        self.username               = args['username']
        self.role                   = args['role']
        self.first_name             = args['first_name']
        self.last_name              = args['last_name']
        self.contact_mobile_number  = args['contact_mobile_number']
        self.contact_email_address  = args['contact_email_address']
        self.address                = args['address']
        self.country                = args['country']
        self.state                  = args['state']
        self.zip_code               = args['zip_code']
        
        self.created_on             = datetime.utcnow()
        self.modified_on            = datetime.utcnow()
        self.created_by             = ''
        self.app_key                = args['app_key']
        self.app_secret             = args['app_secret']

    def to_dict(self):
        user    = {
            'username':                 self.username,
            'role':                     self.role,
            'first_name':               self.first_name,
            'last_name':                self.last_name,
            'contact_mobile_number':    self.contact_mobile_number,
            'contact_email_address':    self.contact_email_address,
            'address':                  self.address,
            'country':                  self.country,
            'state':                    self.state,
            'zip_code':                 self.zip_code,
            'created_on':               str(self.created_on),
            'modified_on':              str(self.modified_on),
            'created_by':               self.created_by,
            'app_key':                  self.app_key,
            'app_secret':               self.app_secret,
        }

        return user

    def get_role(self):
        return 'service_provider'