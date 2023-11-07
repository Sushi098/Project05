from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Faculty
from service.service.AddFacultyService import AddFacultyService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json

class FacultyCtl(BaseCtl):

    def preload(self, request,params={}):
        print("This is Preload")
        courseList = CourseService().preload()
        subjectList = SubjectService().preload()
        collegeList = CollegeService().preload()
        coursedata = []
        for x in courseList:
            coursedata.append(x.to_json())
        subjectdata = []
        for y in subjectList:
            subjectdata.append(y.to_json())
        collegedata = []
        for z in collegeList:
            collegedata.append(z.to_json())
        return JsonResponse({"subpreload":subjectdata,"coupreload":coursedata,"colpreload":collegedata})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] = requestForm["dob"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            self.form["error"] = True
            inputError["firstName"] = "First Name can not be null"
        if (DataValidator.isNull(self.form["lastName"])):
            self.form["error"] = True
            inputError["lastName"] = "Last Name can not be null"
        if (DataValidator.isNull(self.form["email"])):
            self.form["error"] = True
            inputError["email"] = "Email can not be null"
        if(DataValidator.isNotNull(self.form["email"])):
            if(DataValidator.isemail(self.form["email"])):
                self.form["error"] = True
                inputError["email"] = "Email Id must be like abc@gmail.com"
        if (DataValidator.isNull(self.form["password"])):
            self.form["error"] = True
            inputError["password"] = "Password can not be null"
        if (DataValidator.isNull(self.form["address"])):
            self.form["error"] = True
            inputError["address"] = "Address can not be null"
        if (DataValidator.isNull(self.form["gender"])):
            self.form["error"] = True
            inputError["gender"] = "Gender can not be null"
        if (DataValidator.isNull(self.form["dob"])):
            self.form["error"] = True
            inputError["dob"] = "Date of Birth can not be null"
        if(DataValidator.isNotNull(self.form["dob"])):
            if(DataValidator.isDate(self.form["dob"])):
                self.form["error"] = True
                inputError["dob"] = "Incorrect date, should be YYYY-MM-DD"
        if (DataValidator.isNull(self.form["college_ID"])):
            self.form["error"] = True
            inputError["college_ID"] = "College can not be null"            
        if (DataValidator.isNull(self.form["subject_ID"])):
            self.form["error"] = True
            inputError["subject_ID"] = "Subject can not be null"
        if (DataValidator.isNull(self.form["course_ID"])):
            self.form["error"] = True
            inputError["course_ID"] = "course can not be null"
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
        print("Faculty Search ---------------------")
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
            res["LastId"] = Faculty.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        col = CollegeService().get(self.form["college_ID"])
        cou = CourseService().get(self.form["course_ID"])
        sub = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.email = self.form["email"]
        obj.password = self.form["password"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.dob = self.form["dob"]
        obj.college_ID = self.form["college_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.subject_ID = self.form["subject_ID"]
        obj.collegeName = col.collegeName
        obj.courseName = cou.courseName
        obj.subjectName = sub.subjectName
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
                dup = Faculty.objects.exclude(id=self.form["id"]).filter(firstName = self.form["firstName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "First Name already exists"
                else:
                    r = self.form_to_model(Faculty())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
            else:
                duplicate = Faculty.objects.filter(firstName = self.form["firstName"])
                if (duplicate.count() > 0 ):
                    res["error"] = True
                    res["message"] = "First Name already exists"
                else:
                    r = self.form_to_model(Faculty())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})
    
    def get_service(self):
        return AddFacultyService()
