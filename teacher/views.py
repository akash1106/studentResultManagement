from audioop import reverse
from time import time
from unittest import result
from urllib import response
from django.http import  HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mysqlx import Result
from .models import *
import datetime
from json import dumps

def set_cookie(response, key, value, days_expire=30):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires
    )

def Slogin(request): 
    if  request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 's':
                data=tblStudents.objects.filter(studentsName=request.COOKIES['username'],rollId=request.COOKIES['passwd'])
                if data:
                    return HttpResponseRedirect(reverse('shome'))
                else:
                    return render(request,"slogin.html")
            else:
                return HttpResponseRedirect(reverse('plogin'))
        else:
            return render(request,"slogin.html")
    elif request.method=="POST":
        usname=request.POST["username"]
        passwd=request.POST["passwd"]
        data=tblStudents.objects.filter(studentsName=usname,rollId=passwd)
        if(data):
            response=HttpResponseRedirect(reverse('shome'))
            set_cookie(response,'username', usname)
            set_cookie(response,'passwd', passwd)
            set_cookie(response,'log','s')
            return response
        else:
            return render(request,"slogin.html")
def plogin(request):
    if  request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    return HttpResponseRedirect(reverse('phome'))
                else:
                    return render(request,"plogin.html")
        else:
            return render(request,"plogin.html")
    elif request.method=="POST":
        usname=request.POST["username"]
        passwd=request.POST["passwd"]
        data=admin.objects.filter(userName=usname,password=passwd)
        if(data):
            response=HttpResponseRedirect(reverse('phome'))
            set_cookie(response,'username', usname)
            set_cookie(response,'passwd', passwd)
            set_cookie(response,'log','p')
            return response
        else:
            return render(request,"slogin.html")
def shome(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=tblStudents.objects.filter(studentsName=request.COOKIES['username'],rollId=request.COOKIES['passwd'])
            if data:
                l=tblStudents.objects.get(studentsId=data[0].studentsId)
                return render(request,"shome.html",{
                    "student":tblResult.objects.filter(studentId=l),
                    "val":data[0].studentsId,
                })
            else:
                return render(request,"slogin.html")
    return render(request,"empty.html")
def phome(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
            if data:
                return render(request,"phome.html",{
                    "class":tblClasses.objects.all(),
                })
            else:
                return render(request,"slogin.html")
    return render(request,"empty.html")
def addclass(request):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    return render(request,"addclass.html")
                else:
                    return render(request,"slogin.html")
    if request.method=="POST":
        className=request.POST["className"]
        classNameNumeric=request.POST["classNameNumeric"]
        section=request.POST["section"]
        ob1=tblClasses.objects.create(className=className,classNameNumeric=classNameNumeric,section=section,creationDate=datetime.datetime.now(),updationDate=datetime.datetime.now())
        li=tblClasses.objects.all()
        if ob1 not in li:
            tblClasses.save(ob1)
        return HttpResponseRedirect(reverse('phome'))
    return render(request,"empty.html")
def editclass(request,cid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblClasses.objects.filter(id=cid)
                if data and li:
                    return render(request,"editclass.html",{
                        "cid":li[0]
                    })
                else:
                    return render(request,"slogin.html")
    if request.method=="POST":
        className=request.POST["className"]
        classNameNumeric=request.POST["classNameNumeric"]
        section=request.POST["section"]
        ob1=tblClasses.objects.get(id=cid)
        ob1.className=className
        ob1.classNameNumeric=classNameNumeric
        ob1.section=section
        ob1.updationDate=datetime.datetime.now()
        ob1.save()
        return HttpResponseRedirect(reverse('phome'))
    return render(request,"empty.html")
def deleteclass(request,cid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblClasses.objects.filter(id=cid)
                if data and li:
                    li[0].delete()
                    return HttpResponseRedirect(reverse('phome'))
                else:
                    return render(request,"slogin.html")
    return render(request,"empty.html")
def subject(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
            if data:
                return render(request,"subject.html",{
                    "cla1":tblSubjectCombination.objects.all(),
                })
            else:
                return render(request,"slogin.html")
    return render(request,"empty.html")
def addsubject(request):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    return render(request,"addsubject.html")
                else:
                    return render(request,"plogin.html")
    if request.method=="POST":
        subjectName=request.POST["subjectName"]
        subjectCode=request.POST["subjectCode"]
        classId=request.POST["classId"]
        ob1=tblSubjects.objects.create(subjectName=subjectName,subjectCode=subjectCode,creationDate=datetime.datetime.now(),updationDate=datetime.datetime.now())
        ob2=tblSubjectCombination.objects.create(classId=tblClasses.objects.get(id=classId),subjectId=ob1,status=1, creationDate=datetime.datetime.now(),updationDate=datetime.datetime.now())
        li1=tblSubjectCombination.objects.all()
        li=tblSubjects.objects.all()
        if ob1 not in li:
            tblSubjects.save(ob1)
        if ob2 not in li1:
            tblSubjectCombination.save(ob2)
        return HttpResponseRedirect(reverse('phome'))
    return render(request,"empty.html")
def changestatus(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    ob1=tblSubjectCombination.objects.get(id=sid)
                    if ob1.status==1:
                        ob1.status=0
                    else:
                        ob1.status=1
                    ob1.save()
                else:
                    return render(request,"plogin.html")
    return HttpResponseRedirect(reverse('phome'))
def editsubject(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblSubjectCombination.objects.filter(id=sid)
                if data and li:
                    return render(request,"editsubject.html",{
                        "cid":li[0]
                    })
                else:
                    return render(request,"slogin.html")
    if request.method=="POST":
        subjectName=request.POST["subjectName"]
        subjectCode=request.POST["subjectCode"]
        classId=request.POST["classId"]
        ob1=tblSubjectCombination.objects.get(id=sid)
        ob2=ob1.subjectId
        ob2.subjectName=subjectName
        ob2.subjectCode=subjectCode
        ob2.updationDate=datetime.datetime.now()
        ob2.save()
        ob1.classId=tblClasses.objects.get(id=classId)
        ob1.updationDate=datetime.datetime.now()
        ob1.save()
        return HttpResponseRedirect(reverse('phome'))
    return render(request,"empty.html")
def deletesubject(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblSubjectCombination.objects.get(id=sid)
                l1=li.subjectId
                if data and li:
                    li.delete()
                    l1.delete()
                    return HttpResponseRedirect(reverse('phome'))
                else:
                    return render(request,"slogin.html")
    return render(request,"empty.html")
def student(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
            if data:
                return render(request,"student.html",{
                    "student":tblStudents.objects.all(),
                })
            else:
                return render(request,"plogin.html")
    return render(request,"empty.html")
def addstudent(request):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    return render(request,"addstudent.html")
                else:
                    return render(request,"plogin.html")
    if request.method=="POST":
        studentsName=request.POST["studentsName"]
        rollId=request.POST["rollId"]
        studentsEmail=request.POST["studentsEmail"]
        gender=request.POST["gender"]
        DOB1=request.POST["DOB"]
        classId=request.POST["classId"]
        ob1=tblStudents.objects.create(studentsName=studentsName,rollId=rollId,studentsEmail=studentsEmail,gender=gender,DOB=DOB1,classId=tblClasses.objects.get(id=classId),regDate=datetime.datetime.now(),updationDate=datetime.datetime.now(),status=1)
        l1=tblStudents.objects.all()
        if ob1 not in l1:
            tblStudents.save(ob1)
        li1=tblSubjectCombination.objects.filter(classId=tblClasses.objects.get(id=classId))
        for i in li1:
            ob=tblResult.objects.create(studentId=ob1,classId=tblClasses.objects.get(id=classId),mark=0,subjectId=i.subjectId,status=0,creationDate=datetime.datetime.now(),updationDate=datetime.datetime.now())
            tblResult.save(ob)
        return HttpResponseRedirect(reverse('phome'))
def editstudent(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblStudents.objects.get(studentsId=sid)
                if data and li:
                    return render(request,"editstudent.html",{
                        "stu":li
                    })
                else:
                    return render(request,"plogin.html")
    if request.method=="POST":
        studentsName=request.POST["studentsName"]
        rollId=request.POST["rollId"]
        studentsEmail=request.POST["studentsEmail"]
        gender=request.POST["gender"]
        DOB1=request.POST["DOB"]
        classId=request.POST["classId"]
        ob1=tblStudents.objects.get(studentsId=sid)
        ob1.studentsName=studentsName
        ob1.rollId=rollId
        ob1.studentsEmail=studentsEmail
        ob1.gender=gender
        ob1.DOB=DOB1
        ob1.classId=tblClasses.objects.get(id=classId)
        ob1.save()
        return HttpResponseRedirect(reverse('phome'))
    return render(request,"empty.html")
def changestatuss(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    ob1=tblStudents.objects.get(studentsId=sid)
                    if ob1.status==1:
                        ob1.status=0
                    else:
                        ob1.status=1
                    ob1.save()
                else:
                    return render(request,"plogin.html")
    return HttpResponseRedirect(reverse('phome'))
def deletestudent(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                li=tblStudents.objects.get(studentsId=sid)
                if data and li:
                    li.delete()
                    return HttpResponseRedirect(reverse('phome'))
                else:
                    return render(request,"slogin.html")
    return render(request,"empty.html")
def markstudent(request,sid):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    l=tblStudents.objects.get(studentsId=sid)
                    return render(request,"markp.html",{
                        "student":tblResult.objects.filter(studentId=l),
                        "val":sid,
                    })
                else:
                    return render(request,"plogin.html")
    if request.method=="POST":
        l=tblStudents.objects.get(studentsId=sid)
        lis=tblResult.objects.filter(studentId=l)
        for i in lis:
            mark=request.POST[str(i.subjectId.subjectName)]
            i.mark=mark
            i.save()
        return HttpResponseRedirect(reverse('plogin'))
    return render(request,"empty.html")
def changepass(request):
    if request.method=="GET":
        if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
            if request.COOKIES['log'] == 'p':
                data=admin.objects.filter(userName=request.COOKIES['username'],password=request.COOKIES['passwd'])
                if data:
                    return render(request,"changepass.html")
                else:
                    return render(request,"plogin.html")
    if request.method=="POST":
        oldpass=request.POST["password"]
        newpass=request.POST["newpassword"]
        ob1=admin.objects.get(id=1)
        if ob1.password==oldpass:
            ob1.password=newpass
            ob1.save()
        return HttpResponseRedirect(reverse('plogin'))
    return render(request,"empty.html")
def logoutp(request):
    response=HttpResponseRedirect(reverse('plogin'))
    response.delete_cookie("username")
    response.delete_cookie("passwd")
    response.delete_cookie("log")
    return response
def logouts(request):
    response=HttpResponseRedirect(reverse('slogin'))
    response.delete_cookie("username")
    response.delete_cookie("passwd")
    response.delete_cookie("log")
    return response
def empty(request):
    return render(request,"empty.html")