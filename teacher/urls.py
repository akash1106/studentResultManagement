from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('',views.Slogin,name="slogin"),
  path('shome/',views.shome,name="shome"),
  path('plogin/',views.plogin,name="plogin"),
  path('phome/',views.phome,name="phome"),
  path('addclass/',views.addclass,name="addclass"),
  path('editclass/<int:cid>/',views.editclass,name="editclass"),
  path('deleteclass/<int:cid>/',views.deleteclass,name="deleteclass"),
  path('subject/',views.subject,name="subject"),
  path('addsubject/',views.addsubject,name="addsubject"),
  path('changestatus/<int:sid>/',views.changestatus,name="changestatus"),
  path('editsubject/<int:sid>/',views.editsubject,name="editsubject"),
  path('deletesubject/<int:sid>/',views.deletesubject,name="deletesubject"),
  path('student/',views.student,name="student"),
  path('empty/',views.empty,name="empty")
]