from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse_lazy

from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'homepage.html')


def about(request):

    return render(request, 'about.html')

def contactus(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "contact.html")


@csrf_exempt
def loginpage(request):

    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                print("Succesful")
                return redirect('adminhome')
            elif user is not None:
                login(request, user)
                error = "no"
                g = request.user.groups.all()[0].name
                if g == 'Doctor':
                    return redirect('patientdash')
                elif g == 'Patient':
                    return redirect('patientdash')
            else:
                print('something is wrong')
                error = "yes"
                print(e)
        except Exception as e:
            error = "yes"
            print(e)
            #raise e
    return render(request, 'login1.html')


def createAcc(request):
    error = ""
    user = "none"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST.get('repassword')
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        username = request.POST['username']
        bloodgroup = request.POST['bloodgroup']
        try:
            if password == repassword:
                Patient.objects.create(name=name, email=email, username=username, password=password,
                                       repassword=repassword, gender=gender, phonenumber=phonenumber, bloodgroup=bloodgroup)
                user = User.objects.create_user(
                    first_name=name, email=email, password=password, username=username)
                pat_group = Group.objects.get(name='Patient')
                pat_group.user_set.add(user)
                # print(pat_group)
                user.save()
                # print(user)
                error = "no"
            else:
                error = "yes"

        except Exception as e:
            error = "yes"
            # print("Error:",e)
    d = {'error': error}
    # print(error)
    return render(request, 'createAcc.html', d)
    # return render(request,'createaccount.html')




def services(request):
    return render(request, 'services.html')


def logoutpg(request):
    logout(request)
    return redirect('login')


def patientinfo(request):
    if not request.user.is_active:
        return redirect('login')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(username=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'patientinfo.html', d)
    elif g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(username=request.user)
        d = {'doctor_details': doctor_details}
        return render(request, 'doctorinfo.html', d)


def patientdash(request):
    if not request.user.is_active:
        return redirect('login')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(username=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'patientdash.html', d)
    elif g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(username=request.user)
        d = {'doctor_details': doctor_details}
        return render(request, 'doctorhome.html', d)


def patientprofile(request):

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(username=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'patientprofile.html', d)
    elif g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(username=request.user)
        d = {'doctor_details': doctor_details}
        return render(request, 'doctorprofile.html', d)


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('patientdash')


def updateprofile(request):
    if not request.user.is_active:
        return redirect('login')
    error = ""
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        pat = Patient.objects.all().filter(username=request.user)
        if request.method == 'POST' and request.FILES['image']:

            name = request.POST['name']
            email = request.POST['email']
            gender = request.POST['gender']
            phonenumber = request.POST['phonenumber']
            username = request.POST['username']
            bloodgroup = request.POST['bloodgroup']
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            print(filename)
            print(uploaded_file_url)
            try:
                Patient.objects.filter(username=request.user).update(
                    name=name, email=email, gender=gender, phonenumber=phonenumber,
                    username=username, bloodgroup=bloodgroup,profileimg= image)
                # print(user)
                error = "no"
            except Exception as e:
                error = "yes"
                print("Error:",e)
        d = {'error': error, 'pat': pat}
    # print(error)
        return render(request, 'updatepatient.html', d)

    elif g == 'Doctor':
        doc = Doctor.objects.filter(username=request.user)
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            username = request.POST['username']

            gender = request.POST['gender']
            phonenumber = request.POST['phonenumber']
            address = request.POST['address']

            bloodgroup = request.POST['bloodgroup']
            specialization = request.POST['specialization']
            image1 = request.FILES['image1']
            fs1 = FileSystemStorage()
            filename1 = fs1.save(image1.name, image1)
            uploaded_file_url_1 = fs1.url(filename1)
            print(filename1)
            print(uploaded_file_url_1)
            try:
                Doctor.objects.filter(username=request.user).update(name=name, email=email, gender=gender, username=username,
                                                                    phonenumber=phonenumber, address=address, bloodgroup=bloodgroup, specialization=specialization,
                                                                    profileimg = image1)
                error = "no"
            except Exception as e:
                error = "yes"
                print("Error:", e)
        d = {'error': error, 'doc': doc}
    # print(error)
        return render(request, 'updatedoctor.html', d)



def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('login')
    alldoctors = Doctor.objects.all()


    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(username=request.user)
        d = {'alldoctors': alldoctors,'patient_details': patient_details}
        if request.method == 'POST':

            doctorname = request.POST['doctorname']
            username = request.POST['username']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            gender = request.POST['gender']
            a = Appointment.objects.filter(
                appointmentdate=appointmentdate,appointmenttime=appointmenttime).count()
            print(a)
            if a <= 1:

                try:
                    Appointment.objects.create(doctorname=doctorname, username=username, patientemail=patientemail,
                                               appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, gender=gender)
                    error = "no"
                except Exception as ex:
                    error = "yes"
                    print(ex)
            else:
                error = "yes"
                print(error)

            e = {"error": error, "patient_details": patient_details}

            return render(request, 'patientmakeappointments.html', e)
        elif request.method == 'GET':
            return render(request, 'patientmakeappointments.html', d)


def viewappointments(request):
    if not request.user.is_active:
        return redirect('login')
    # print(request.user)
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(username=request.user)
        u = Appointment.objects.all().filter(username=request.user,
                                             appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
        st = {
            "stu": u,"patient_details":patient_details
        }
        return render(request, 'patientviewappointments.html', st)
    elif g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(username=request.user)
        y = Doctor.objects.all().filter(username=request.user).values_list('name', flat=True)

        u = Appointment.objects.all().filter(
            doctorname=y[0], appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
        st = {
            "stu": u,"doctor_details":doctor_details
        }
        return render(request, 'doctorviewapp.html', st)


def add_prescrip(request, pid):
    if not request.user.is_active:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        weight = request.POST['weight']
        bp = request.POST['bp']
        city = request.POST['city']
        count = request.POST['count']
        gender = request.POST['gender']
        print(type(count))
        count = int(count)
        print(type(count))
        try:
            for i in range(count):
                i = i+1
                medname = request.POST[f'medname{i}']
                medmg = request.POST[f'mg{i}']
                dose = request.POST[f'dose{i}']
                comment = request.POST[f'comment{i}']
                print(pid)
                Medicine.objects.create(
                    appid=pid, medname=medname, medmg=medmg, dose=dose, comment=comment)
            Prescription.objects.create(
                name=name, age=age, weight=weight, bp=bp, city=city, appid=pid)
            Appointment.objects.filter(id=pid).update(status=False)
            error = "no"

        except Exception as ex:
            error = "yes"
            print(ex)
        print(error)
        e = {"error": error}
        return render(request, 'prescription.html', e)

    return render(request, 'prescription.html')


def patient_history(request):
    if not request.user.is_active:
        return redirect('login')
    # print(request.user)
    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        y = Doctor.objects.all().filter(username=request.user).values_list('name', flat=True)
        doctor_details = Doctor.objects.all().filter(username=request.user)
        u = Appointment.objects.all().filter(doctorname=y[0], appointmentdate__lt=timezone.now()).order_by(
            'appointmentdate') | Appointment.objects.all().filter(doctorname=y[0], status=False).order_by('appointmentdate')
        st = {
            "stu": u,"doctor_details":doctor_details
        }
        return render(request, 'doctor_viewpathis.html', st)


def view_prescrip(request, pid):
    if not request.user.is_active:
        return redirect('login')
    prescrip = Prescription.objects.filter(appid=pid)
    med = Medicine.objects.filter(appid=pid)
    p = {'prescrip': prescrip, 'med': med}

    return render(request, 'view_prescription.html', p)


def temp(request):
    pd = Patient.objects.all().count()
    dd = Doctor.objects.all().count()
    gt = {"pd": pd, "dd": dd}
    return render(request, 'temp.html', gt)


def patient_delete_appointment(request, pid):
    if not request.user.is_active:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('viewappointments')


def adminhome(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    doc_count = Doctor.objects.all().count()
    patient = Patient.objects.all()
    patient_count = Patient.objects.all().count()
    appointment = Appointment.objects.filter(
        appointmentdate__gte=timezone.now(), status=True).count()
    appointmentlist = Appointment.objects.filter(
        appointmentdate=timezone.now(), status=True)
    total = patient_count+doc_count
    mydict = {
        'doc': doc,
        'doc_count': doc_count,
        'patient': patient,
        'patient_count': patient_count,
        'appointment': appointment,
        'total': total,
        'appointmentlist': appointmentlist
    }
    return render(request, 'adminDash.html', context=mydict)


def adminaddpatient(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatpassword = request.POST['repassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']

        try:
            if password == repeatpassword:
                Patient.objects.create(name=name, email=email, password=password,
                                       gender=gender, username=username, phonenumber=phonenumber)
                user = User.objects.create_user(
                    first_name=name, email=email, password=password, username=username)
                doc_group = Group.objects.get(name='Patient')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
            print(e)
    d = {'error': error}
    return render(request, 'adminaddpatient.html')


def adminviewpatient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    p = {'pat': pat}
    return render(request, 'adminviewpatient.html', p)


def admin_delete_patient(request, pid, username):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    users = User.objects.filter(username=username)
    users.delete()
    return redirect('adminviewpatient')


def adminadddoctor(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatpassword = request.POST['repassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['birthdate']
        bloodgroup = request.POST['bloodgroup']
        specialization = request.POST['specialization']

        try:
            if password == repeatpassword:
                Doctor.objects.create(name=name, email=email, password=password, gender=gender, username=username, phonenumber=phonenumber,
                                      address=address, birthdate=birthdate, bloodgroup=bloodgroup, specialization=specialization)
                user = User.objects.create_user(
                    first_name=name, email=email, password=password, username=username)
                doc_group = Group.objects.get(name='Doctor')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
            print(e)
    d = {'error': error}
    return render(request, 'adminadddoctor.html', d)


def adminviewdoctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'adminviewdoctor.html', d)


def admin_delete_doctor(request, pid, username):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    users = User.objects.filter(username=username)
    users.delete()
    return redirect('adminviewdoctor')


def adminappointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appoin = Appointment.objects.filter(
        appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
    d = {'appoin': appoin}
    return render(request, 'adminappointment.html', d)

def admin_delete_appointment(request, pid):
    if not request.user.is_active:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('adminappointment')

