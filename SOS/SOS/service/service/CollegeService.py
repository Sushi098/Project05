import re
from unittest import result
from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains College Business Logic
'''

class CollegeService(BaseService):

    def get_model(self):
        return College

    def search(self, params={}):
        pageNo = (params['pageNo'] -1)* self.pageSize
        sql = "select * from ors_college where 1=1"
        val = params.get('collegeName', None)
        if DataValidator.isNotNull(val):
            sql += " and collegeName = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("------------->>", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo']-1)*self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'collegeName', "collegeAddress", 'collegeState', 'collegeCity', 'collegePhoneNumber')
        res = {
            'data':[]
        }
        count=0
        for x in result:
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i,_ in enumerate(x)})
        print("MMMMMMM----------->>", params.get('MaxId'))
        return res
