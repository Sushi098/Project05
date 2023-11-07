from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Student business logics
'''
class RoleService(BaseService):

    def get_model(self):
        return Role

    def search(self,params):
        pageNo = (params['pageNo']-1) * self.pageSize
        sql = "select * from ors_role where 1=1"
        val = params.get('name', None)
        if(DataValidator.isNotNull(val)):
            sql += "and name = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("--------------->",sql,pageNo,self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'description')
        res = {
            'data': []
        }
        count=0
        for x in result:
            # print({columnName[i]: x[i] for i,_ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i,_ in enumerate(x)})
        return res
