"""HMSFY2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Hosp.views import *
from Hosp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('about/', about,name="AboutUs"),
    path('login/', views.loginpage,name="login"),
    path('createAcc/', createAcc,name="createAcc"),
    path('contactus/',contactus,name="contactus"),
    path('services/',services,name="services"),
    path('patientinfo/',patientinfo,name="patientinfo"),
    path('patientdash/',patientdash,name="patientdash"),
    path('logoutpg/',logoutpg,name='logoutpg'),
    path('patientprofile/',patientprofile,name="patientprofile"),
    path('makeappointments/',MakeAppointments,name='makeappointments'),
    path('viewappointments/',viewappointments,name='viewappointments'),
    path('patienthistory/',patient_history,name='patienthistory'),
    path('PatientDeleteAppointment<int:pid>',patient_delete_appointment,name='patient_delete_appointment'),
    path('adminaddpatient/',adminaddpatient,name='adminaddpatient'),
    path('adminadddoctor/',adminadddoctor,name='adminadddoctor'),
    path('adminhome/',adminhome,name='adminhome'),
    path('adminviewpatient/',adminviewpatient,name='adminviewpatient'),
    path('adminviewdoctor/',adminviewdoctor,name='adminviewdoctor'),
    path('adminappointment/',adminappointment,name='adminappointment'),
    path('adminDeleteDoctor<int:pid><str:username>',admin_delete_doctor,name='admin_delete_doctor'),
    path('adminDeletepatient<int:pid><str:username>',admin_delete_patient,name='admin_delete_patient'),
    path('prescription<int:pid>/',add_prescrip,name='add_prescrip'),
    path('view_prescription<int:pid>/',view_prescrip,name='view_prescrip'),
    path('temp/',temp,name='temp'),
    path('updatepatient/',updateprofile,name='updateprofile'),


#change password

path('password/',PasswordChangeView.as_view(),name='change_password'),


    #reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
