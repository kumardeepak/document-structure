import json
from datetime import datetime

class UserAdmin:
    def __init__(self, args):

        self.username               = args['username']
        self.password               = args['password']
        self.role                   = args['role']
        self.first_name             = args['first_name']
        self.last_name              = args['last_name']
        self.created_on             = datetime.utcnow()
        self.modified_on            = datetime.utcnow()

        self.created_by             = 'FVS'
        self.salt                   = ''

    def to_dict(self, with_password=False):
        user    = {
            'username':                 self.username,
            'salt':                     self.salt,
            'role':                     self.role,
            'first_name':               self.first_name,
            'last_name':                self.last_name,
            'created_by':               self.created_by,
            'created_on':               str(self.created_on),
            'modified_on':              str(self.modified_on),
        }
        if with_password:
            user['password'] = self.password
            
        return user

    def get_role(self):
        return 'admin'