
from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from django.http.response import JsonResponse
import json

class TimeTableCtl(BaseCtl):
    def preload(self, request,params={}):
        courseList = CourseService().preload()
        subjectList = SubjectService().preload()
        coursedata = []
        for x in courseList:
            coursedata.append(x.to_json())
        subpreload = []
        for y in subjectList:
            subpreload.append(y.to_json())
        return JsonResponse({"subpreload":subpreload,"coupreload":coursedata})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["examTime"] = requestForm["examTime"]
        self.form["examDate"] = requestForm["examDate"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        self.form["semester"] = requestForm["semester"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["examTime"])):
            self.form["error"] = True
            inputError["examTime"] = "Time can not be null"
        if(DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "Date can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["semester"])):
            inputError["semester"] = "Semester can not be null"
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
            params["semester"] = json_request.get("semester",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = TimeTable.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.examTime = self.form["examTime"]
        obj.examDate = self.form["examDate"]
        obj.semester = self.form["semester"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.subjectName = s.subjectName
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
                dup = TimeTable.objects.exclude(id=self.form["id"]).filter(subject_ID= self.form["subject_ID"],examTime=self.form["examTime"],examDate=self.form["examDate"])
                if (dup.count()>0):
                    res["error"] = True
                    res["message"] = "Exam time and date was already set for this subject"
                else:
                    r = self.form_to_model(TimeTable())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated successfully"
            else:
                duplicate = TimeTable.objects.filter(subject_ID=self.form["subject_ID"],examTime=self.form["examTime"],examDate=self.form["examDate"])
                if (duplicate.count()>0):
                    res["error"] = True
                    res["message"] = "Exam time and date was already set for this subject"
                else:
                    r = self.form_to_model(TimeTable())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})


    def get_service(self):
        return TimeTableService()
