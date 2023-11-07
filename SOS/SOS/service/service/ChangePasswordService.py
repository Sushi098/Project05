from collections import UserList
from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains user business logics.
'''

class ChangePasswordService(BaseService):

    def authenticate(self, params):
        UserList = self.search(params)
        if(UserList.count() > 0 ):
            print("8888888->", UserList[0].login_id)
            return UserList[0]
        else:
            return None


    def get_model(self):
        return User
