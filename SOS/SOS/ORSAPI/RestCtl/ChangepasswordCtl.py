from .BaseCtl import BaseCtl
from ORSAPI.utility.Datavalidator import DataValidator
from service.service.UserService import UserService
from service.service.EmailMessage import EmailMessage
from service.service.EmailService import EmailService
from service.models import User
import json
from django.http.response import JsonResponse

class ChangepasswordCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm.get("login_id",None)
        self.form["oldPassword"] = requestForm.get("oldPassword",None)
        self.form["newPassword"] = requestForm.get("newPassword",None)
        self.form["confirmPassword"] = requestForm.get("confirmPassword",None)

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["oldPassword"])):
            self.form["error"] = True
            inputError["oldPassword"] = "Password can not be Null"
        if (DataValidator.isNull(self.form["newPassword"])):
            self.form["error"] = True
            inputError["newPassword"] = " Password can not be Null"
        if (DataValidator.isNull(self.form["confirmPassword"])):
            self.form["error"] = True
            inputError["confirmPassword"] = "Password can not be Null"
        return self.form["error"]


    def submit(self, request,params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        if self.input_validation():
            self.form["error"] = True
            self.form["message"] = ""
        else:
            obj = User.objects.filter(login_id = self.form["login_id"], password = self.form["oldPassword"])
            print("passwordkjkfk----->>", obj)
            if obj.count()>0:
                obj = obj[0]
                if self.form["newPassword"] == self.form["confirmPassword"]:
                    convertUser = self.convert(obj,obj.id,self.form["newPassword"],self.form["confirmPassword"])
                    UserService().save(convertUser)
                    emsg = EmailMessage()
                    emsg.to = [obj.login_id]
                    emsg.subject = "Change Password"
                    mailResponse = EmailService.send(emsg,"changePassword",obj)
                    if mailResponse == 1:
                        self.form["error"] = False
                        self.form["message"] = "Your password has been changed successfully,Please Check your mail"
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Please Check Your Internet Connection"
                else:
                    self.form["error"] = True
                    self.form["message"] = "Confirm password wasn't matched"
            else:
                self.form["error"] = True
                self.form["message"] = "Old Password is wrong"
        return JsonResponse({"form":self.form})


    
    def convert(self,u,uid,unpwd,ucpwd):
        u.id = uid
        u.password = unpwd
        u.confirmpassword = ucpwd
        return u
