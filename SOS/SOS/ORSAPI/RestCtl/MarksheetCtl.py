from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService
from service.service.MarksheetMeritListService import MarksheetMeritListService
from django.http.response import JsonResponse
import json

class MarksheetCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["rollNumber"])):
            self.form["error"] = True
            inputError["rollNumber"] = "Roll No can not be null"
        if (DataValidator.isNotNull(self.form["rollNumber"])):
            if (DataValidator.ischeckroll(self.form["rollNumber"])):
                self.form["error"] = True
                inputError["rollNumber"] = "Enter correct roll no"
        if (DataValidator.isNull(self.form["name"])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null"
        if (DataValidator.isNull(self.form["physics"])):
            self.form["error"] = True
            inputError["physics"] = "Physics can not be null"
        if (DataValidator.isNotNull(self.form["physics"])):
            if (DataValidator.ischeck(self.form["physics"])):
                self.form["error"] = True
                inputError["physics"] = "Enter correct marks"
        if (DataValidator.isNull(self.form["chemistry"])):
            self.form["error"] = True
            inputError["chemistry"] = "Chemistry can not be null"
        if (DataValidator.isNotNull(self.form["chemistry"])):
            if (DataValidator.ischeck(self.form["chemistry"])):
                self.form["error"] = True
                inputError["chemistry"] = "Enter correct marks"
        if (DataValidator.isNull(self.form["maths"])):
            self.form["error"] = True
            inputError["maths"] = "Maths can not be null"
        if (DataValidator.isNotNull(self.form["maths"])):
            if (DataValidator.ischeck(self.form["maths"])):
                self.form["error"] = True
                inputError["maths"] = "Enter correct marks"
        return self.form["error"]

    def get(self,request,params={}):
        r = self.get_service().get(params["id"])
        res = {}
        if (r != None):
            res["data"] = r.to_json()
            res["error"] = False
            res["message"] = "Data found"
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":res["data"]})

    def delete(self,request,params={}):
        r = self.get_service().get(params["id"])
        res = {}
        if (r != None):
            self.get_service().delete(params["id"])
            res["data"] = r.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data":res})

    def search(self,request,params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["rollNumber"] = json_request.get("rollNumber",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Marksheet.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["error"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.rollNumber = self.form["rollNumber"]
        obj.name = self.form["name"]
        obj.physics = self.form["physics"]
        obj.chemistry = self.form["chemistry"]
        obj.maths = self.form["maths"]
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
                dup = Marksheet.objects.exclude(id=self.form["id"]).filter(rollNumber = self.form["rollNumber"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Roll number already exists"
                else:
                    r = self.form_to_model(Marksheet())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
            else:
                duplicate = Marksheet.objects.filter(rollNumber = self.form["rollNumber"])
                if (duplicate.count() > 0 ):
                    res["error"] = True
                    res["message"] = "Roll number already exists"
                else:
                    r = self.form_to_model(Marksheet())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})


    def meritList(self,request,params={}):
        params["pageNo"] = 1
        c = MarksheetMeritListService().search(params)
        res = {}
        if ( c != None):
            res["data"] = c["data"]
        return JsonResponse({"merit":res["data"]})

    def get_service(self):
        return MarksheetService()


