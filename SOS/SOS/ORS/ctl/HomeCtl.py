from django.http import HttpResponse
from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl

class HomeCtl(BaseCtl):

    def display(self, request, params={}):
        print("--------------------Home CTL Display>>>>",self,request)
        return render(request, self.get_template())

        # Template html of Role page    
    def get_template(self):
        return "Home.html"

    def submit(self, request, params={}):
        pass

        # Service of Role     
    def get_service(self):
        return "RoleService()"
