from django.db import models

# Create your models here.
class admin(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    userName=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    updationDate=models.DateTimeField()

class tblClasses(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    className=models.CharField(max_length=100)
    classNameNumeric=models.IntegerField()
    section=models.CharField(max_length=5)
    creationDate=models.DateTimeField()
    updationDate=models.DateTimeField()

class tblStudents(models.Model):
    studentsId=models.AutoField(primary_key=True,unique=True)
    studentsName=models.CharField(max_length=100)
    rollId=models.CharField(max_length=100)
    studentsEmail=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    DOB=models.CharField(max_length=100)
    classId=models.ForeignKey(tblClasses,on_delete=models.CASCADE)
    regDate=models.DateTimeField()
    updationDate=models.DateTimeField()
    status=models.IntegerField()

class tblSubjects(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    subjectName=models.CharField(max_length=100)
    subjectCode=models.CharField(max_length=100)
    creationDate=models.DateTimeField()
    updationDate=models.DateTimeField()

class tblSubjectCombination(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    classId=models.ForeignKey(tblClasses,on_delete=models.CASCADE)
    subjectId=models.ForeignKey(tblSubjects,on_delete=models.CASCADE)
    status=models.IntegerField()
    creationDate=models.DateTimeField()
    updationDate=models.DateTimeField()

class tblResult(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    studentId=models.ForeignKey(tblStudents,on_delete=models.CASCADE)
    classId=models.ForeignKey(tblClasses,on_delete=models.CASCADE)
    subjectId=models.ForeignKey(tblSubjects,on_delete=models.CASCADE)
    mark=models.IntegerField()
    status=models.IntegerField()
    creationDate=models.DateTimeField()
    updationDate=models.DateTimeField()
    