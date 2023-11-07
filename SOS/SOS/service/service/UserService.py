from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains User business logics.   
'''

class UserService(BaseService):
    def authenticate(self, params={}):
        print("----auth--params-->",params)
        userList = self.search2(params)
        if (userList.count() == 1):
            print("----userList-0-index-->",userList[0])
            return userList[0]
        else:
            return None
        
    def search2(self, params):

        q = self.get_model().objects.filter()

        val = params.get("login_id", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(login_id=val)
            print("----q--->>",q)
        
        val = params.get("password", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(password=val)

        return q

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from sos_user where 1=1"
        val = params.get("login_id", None)
        print("-----val-->>",val)
        if DataValidator.isNotNull(val):
            sql += " and login_id = '"+val+"' "
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "firstName", "lastName", "login_id", "password", "confirmpassword",
                      "dob", "address", "gender", "mobilenumber", "role_Id", "role_Name")
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnName[i]:  x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return User 
