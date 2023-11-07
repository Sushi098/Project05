from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Subject
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from django.http.response import JsonResponse
import json

class SubjectCtl(BaseCtl):
    def preload(self, request,params={}):
        self.data = CourseService().preload()
        preloadList = []
        for x in self.data:
            preloadList.append(x.to_json())
        return JsonResponse({"preloadList":preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDescription"] = requestForm["subjectDescription"]
        self.form["course_ID"] = requestForm["course_ID"]

    def input_validation(self):
        # super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["subjectName"])):
            self.form["error"] = True
            inputError["subjectName"] = "Name can not be null"
        if(DataValidator.isNull(self.form["subjectDescription"])):
            inputError["subjectDescription"] = "Description can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course can not be null"
            self.form["error"] = True
        return self.form["error"]

    def get(self, request,params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if (c != None):
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data found"
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":res["data"]}) 

    def delete(self, request,params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if (c != None):
            self.get_service().delete(params["id"])
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data":res})

    def search(self, request,params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["subjectName"] = json_request.get("subjectName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Subject.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"]  = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.subjectName = self.form["subjectName"]
        obj.subjectDescription = self.form["subjectDescription"]
        obj.course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
        return obj

    def save(self,request,params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"]>0):
                dup = Subject.objects.exclude(id=self.form["id"]).filter(subjectName = self.form["subjectName"])
                if (dup.count()>0):
                    res["error"] = True
                    res["message"] = "Subject already exists"
                else:
                    r = self.form_to_model(Subject())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated successfully"
            else:
                duplicate = Subject.objects.filter(subjectName = self.form["subjectName"])
                if (duplicate.count()>0):
                    res["error"] = True
                    res["message"] = "Subject already exists"
                else:
                    r = self.form_to_model(Subject())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})


    def get_service(self):
        return SubjectService()


