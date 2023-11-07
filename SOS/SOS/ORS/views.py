from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

from .ctl.HomeCtl import HomeCtl
from .ctl.BaseCtl import BaseCtl
from .ctl.LoginCtl import LoginCtl
from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl
from .ctl.UserCtl import UserCtl
from .ctl.UserListCtl import UserListCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.CollegeListCtl import CollegeListCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.CourseListCtl import CourseListCtl

from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.MarksheetListCtl import MarksheetListCtl
from .ctl.MarksheetMeritListCtl import MarksheetMeritListCtl

from .ctl.RoleCtl import RoleCtl
from .ctl.RoleListCtl import RoleListCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.SubjectListCtl import SubjectListCtl
from .ctl.AddFacultyCtl import AddFacultyCtl
from .ctl.AddFacultyListCtl import AddFacultyListCtl
from .ctl.TimeTableCtl import TimeTableCtl
from .ctl.TimeTableListCtl import TimeTableListCtl
from .ctl.MyProfileCtl import MyProfileCtl

# Create your views here.
'''
calls respective controller with id
'''
@csrf_exempt
def actionId(request, page="", operation="", id=0):
    path = request.META.get("PATH_INFO")
    print("------------path>>>>>",path)
    if request.session.get("user") is not None and page != "":
        print("---------actionId path is:-",path)
        ctlName= page + "Ctl()"
        ctlObj= eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id": id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        print("-------->>CtlObject",ctlObj)
        res = ctlObj.execute(request, {'id': id})
    elif page == "Home":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id": id})

    elif page == "ForgetPassword":
        ctlName = "ForgetPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id,})
    elif page == "Login":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request,{"id":id, })

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = "Your Session has been Expired, Please Login again"
        res = ctlObj.execute(request, {"id": id, 'path': path})
    return res
    
@csrf_exempt
def auth(request, page="", operation="", id=0):
    print("------auth(request, page="", operation="", id=0):-->>",request, page, operation, id)
    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        out = "LOGOUT SUCCESSFULL"
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation, 'out': out})

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = "Your Session has been Expired, Please Login again"
        res = ctlObj.execute(request, {"id": id})
    return res

def index(request):
    print("--------index_called----->>")
    return render(request,"project.html")

# To remove Favicon error
def GET(self):
    return HttpResponse("Hello Guys")