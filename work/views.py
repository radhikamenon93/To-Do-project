from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from work.forms import Register,Signin,Taskform
from work.models import Task
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper
def mylogin(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.user!=request.user:
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper    


class Registerview(View):
    def get(self,request,*args,**kwargs):
        form=Register()
        return render(request,"reg.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=Register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print(form.cleaned_data)
        form=Register()    
        return render(request,"reg.html",{"form":form})   
class Signinview(View):
    def get(self,request,*args,**kwargs):
        form=Signin()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=Signin(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if(user_obj):
                print("valid")
                login(request,user_obj)
                return redirect("index")
            else:
                print("invalid")    

        return render(request,"login.html",{"form":form})
    
@method_decorator(signin_required,name='dispatch')    
class Taskview(View):
    def get(self,request,*args,**kwargs):
        form=Taskform()
        data=Task.objects.filter(user=request.user).order_by('complete')
        return render(request,"index.html",{"form":form,"data":data})
    def post(self,request,*args,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
        data=Task.objects.filter(user=request.user)
        return render(request,"index.html",{"form":form,"data":data})
class Taskupdate(View):
    def get(self,request,*args,**kwargs):  
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.complete == False:
            obj.complete=True
            obj.save()
        elif obj.complete == True:
            obj.complete=False 
            obj.save()   
        return redirect("index")
@method_decorator(mylogin,name="dispatch")    
class Taskdelete(View):
    def get(self,request,*args,**kwargs):  
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        return redirect("index")
class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('login')    
    


    


class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")





