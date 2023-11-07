import pkgutil
from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.models import Role
from service.service.RoleService import RoleService
from django.http.response import JsonResponse
import json

class RoleCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]
    
    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["name"])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null" 
        if (DataValidator.isNull(self.form["description"])):
            self.form["error"] = True
            inputError["description"] = "Description can not be null"
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
            params["name"] = json_request.get("name",None)
            params["pageNo"] = json_request.get("pageNo",None)
        c = self.get_service().search(params)
        res = { "mesg":"" }
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Role.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.description = self.form["description"]
        return obj

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"] > 0):
                dup = Role.objects.exclude(id=self.form["id"]).filter(name = self.form["name"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Role name already exists"
                else:
                    r = self.form_to_model(Role())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
            else:
                duplicate = Role.objects.filter(name = self.form["name"])
                if (duplicate.count() > 0 ):
                    res["error"] = True
                    res["message"] = "Role name already exists"
                else:
                    r = self.form_to_model(Role())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form})


    def get_service(self):
        return RoleService()