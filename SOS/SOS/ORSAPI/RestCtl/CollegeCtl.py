from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import College
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json


class CollegeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['collegeName'] = requestForm["collegeName"]
        self.form['collegeAddress'] = requestForm['collegeAddress']
        self.form['collegeState'] = requestForm["collegeState"]
        self.form['collegeCity'] = requestForm["collegeCity"]
        self.form['collegePhoneNumber'] = requestForm["collegePhoneNumber"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["collegeName"])):
            self.form["error"] = True
            inputError["collegeName"] = "Name can not be null"
        if (DataValidator.isNull(self.form['collegeAddress'])):
            self.form["error"] = True
            inputError["collegeAddress"] = "Address can not be null"
        if (DataValidator.isNull(self.form["collegeState"])):
            self.form["error"] = True
            inputError["collegeState"] = "State can not be null"
        if (DataValidator.isNull(self.form["collegeCity"])):
            self.form["error"] = True
            inputError["collegeCity"] = "City can not be null"
        if (DataValidator.isNull(self.form["collegePhoneNumber"])):
            self.form["error"] = True
            inputError["collegePhoneNumber"] = "Phone Number can not be null"
        if (DataValidator.isNotNull(self.form["collegePhoneNumber"])):
            if(DataValidator.ismobilecheck(self.form["collegePhoneNumber"])):
                self.form["error"] = True
                inputError["collegePhoneNumber"] = "Enter correct phone no"
        return self.form["error"]

    def get(self,request,params={}):
        c = self.get_service().get(params['id'])
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
            res["message"] = "Data has been deleted Successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data":res})

    def search(self,request,params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["collegeName"] = json_request.get("collegeName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = College.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        print("ORS API College ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.collegeName = self.form["collegeName"]
        obj.collegeAddress = self.form["collegeAddress"]
        obj.collegeState = self.form["collegeState"]
        obj.collegeCity = self.form["collegeCity"]
        obj.collegePhoneNumber = self.form["collegePhoneNumber"]
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
                dup = College.objects.exclude(id=self.form['id']).filter(collegeName=self.form["collegeName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "College Name already exists"
                else:
                    r = self.form_to_model(College())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
            else:
                duplicate = College.objects.filter(collegeName = self.form["collegeName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "College Name already exists"
                else:
                    r = self.form_to_model(College())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res, "form":self.form})

    # Service of College
    def get_service(self):
        return CollegeService()
