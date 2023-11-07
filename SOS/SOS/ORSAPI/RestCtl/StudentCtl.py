from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json

class StudentCtl(BaseCtl):
    def preload(self, request,params={}):
        collegeList = CollegeService().preload()
        preloadList = []
        for x in collegeList:
            preloadList.append(x.to_json())
        return JsonResponse({"preloadList":preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobileNumber"] = requestForm["mobileNumber"]
        self.form["email"] = requestForm["email"]
        self.form["college_ID"] = requestForm["college_ID"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            self.form["error"] = True
            inputError["firstName"] = "First Name can not be null"
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last_Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True 
        if(DataValidator.isNotNull(self.form["dob"])):
            if(DataValidator.isDate(self.form["dob"])):
                self.form["error"] = True
                inputError["dob"] = "Incorrect date, should be YYYY-MM-DD"
        if(DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"] = "Mobile No can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["mobileNumber"])):
            if( DataValidator.ismobilecheck(self.form['mobileNumber'])):
                self.form["error"] = True
                inputError["mobileNumber"] = "Enter Correct Mobile No."
        if(DataValidator.isNull(self.form["email"])):
            inputError["email"] = "Email can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["email"])):
            if(DataValidator.isemail(self.form["email"])):
                self.form["error"] = True
                inputError["email"] = "Email Id must be like abc@gmail.com"
        if(DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "College Name can not be null"
            self.form["error"] = True
        return self.form["error"]

    def get(self,request,params={}):
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

    def delete(self,request,params={}):
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

    def search(self,request,params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["firstName"] = json_request.get("firstName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Student.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        c = CollegeService().get(self.form["college_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.dob = self.form["dob"]
        obj.mobileNumber = self.form["mobileNumber"]
        obj.email = self.form["email"]
        obj.college_ID = self.form["college_ID"]
        obj.collegeName = c.collegeName
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
                dup = Student.objects.exclude(id=self.form["id"]).filter(firstName = self.form["firstName"])
                if (dup.count()>0):
                    res["error"] = True
                    res["message"] = "First Name already exists"
                else:
                    r = self.form_to_model(Student())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated successfully"
            else:
                duplicate = Student.objects.filter(firstName = self.form["firstName"])
                if (duplicate.count()>0):
                    res["error"] = True
                    res["message"] = "First Name already exists"
                else:
                    r = self.form_to_model(Student())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})

    def get_service(self):
        return StudentService()
