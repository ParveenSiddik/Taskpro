from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import TaskForm,RegistrationForm,SignInForm

from django.contrib import messages

from myapp.models import Task

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate

from django.utils.decorators import method_decorator

from myapp.decorators import signin_required

from django.db.models import Q,Count

from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        return render(request,"task_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save() # ModelForm provides this option without giving create 

            messages.success(request,"Task Added Successfully")

             
            return redirect("task_list")



        else:

            messages.error(request," Addition Failed")

            return render(request,"task_create.html",{"form":form_instance})

#Task List

@method_decorator(decs,name="dispatch")
class TaskListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category=="all":

            qs=Task.objects.filter(user=request.user)

        else:

            qs=Task.objects.filter(category=selected_category,user=request.user)    

        if search_text!=None:

            qs=Task.objects.filter(user=request.user)

            qs=Task.objects.filter(Q(title_icontains=search_text)|Q(description_icontains=search_text))

        return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})

@method_decorator(decs,name="dispatch")
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"task":qs})

@method_decorator(decs,name="dispatch")
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        # extract pk from kwargs
        id=kwargs.get("pk")

        # fetch task object
        
        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_obj)

        # Adding status field to form

        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select"}),initial=task_obj.status)

        return render(request,"task_edit.html",{"form":form_instance})


    
        #     return redirect("task_list")

        # else:    

        #     return render(request,"task_edit.html",{"form":form_instance})

               # without ORM Query

    def post(self,request,*args,**kwargs):

             # Extract id from Keyword args
        id=kwargs.get("pk")

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(request.POST,instance=task_obj)

        if form_instance.is_valid():

                form_instance.instance.status=request.POST.get("status")

                form_instance.save()

                return redirect("task_list")

        else:

                return render(request,"task_edit.html",{"form":form_instance})



@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        # extract id and delete task object with this id

        Task.objects.get(id=kwargs.get("pk")).delete()

        return redirect("task_list")

@method_decorator(decs,name="dispatch")
class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.filter(user=request.user)

        total_task_count=qs.count()

        category_count=qs.values("category").annotate(cat_count=Count("category"))
        print(category_count)


        status_summary=qs.values("status").annotate(stat_count=Count("status"))
        print(status_summary)

        context={
            "total_task_count":total_task_count,
            "category_summary":category_count,
            "status_summary":status_summary


        }

        return render(request,"task_summary.html",context)        
        

class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("signin")
        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username") 

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

               login(request,user_object)

               return redirect("task_list")

        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')        






