
from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Course, User
from service.service.CourseService import CourseService
from django.http.response import JsonResponse
import json

class CourseCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["courseName"] = requestForm["courseName"]
        self.form["courseDescription"] = requestForm["courseDescription"]
        self.form["courseDuration"] = requestForm["courseDuration"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["courseName"])):
            self.form["error"] = True
            inputError["courseName"] = "Name can not be null"
        if (DataValidator.isNull(self.form["courseDescription"])):
            self.form["error"] = True
            inputError["courseDescription"] = "Description can not be null"
        if (DataValidator.isNull(self.form["courseDuration"])):
            self.form["error"] = True
            inputError["courseDuration"] = "Duration can not be null"
        return self.form["error"]

    def get(self,request,params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if c != None:
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data found"
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":res["data"]})

    def delete(self,request,params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if c != None:
            self.get_service().delete(params["id"])
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted Successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data":res})

    def search(self,request,params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["courseName"] = json_request.get("courseName",None)
            params["pageNo"] = json_request.get("pageNo",None)

        c = self.get_service().search(params)
        res = { "mesg":"" }
        if c != None:
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Course.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.courseName = self.form["courseName"]
        obj.courseDescription = self.form["courseDescription"]
        obj.courseDuration = self.form["courseDuration"]
        return obj

    def save(self,request,params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"] > 0):
                dup = Course.objects.exclude(id=self.form["id"]).filter(courseName = self.form["courseName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Course Name already exists"
                else:
                    r = self.form_to_model(Course())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
            else:
                duplicate = Course.objects.filter(courseName = self.form["courseName"])
                if (duplicate.count() > 0 ):
                    res["error"] = True
                    res["message"] = "Course Name already exists"
                else:
                    r = self.form_to_model(Course())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})

    def get_service(self):
        return CourseService()

    

