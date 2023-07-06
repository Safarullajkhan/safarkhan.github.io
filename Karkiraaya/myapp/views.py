from django.shortcuts import render,redirect
from django.http import HttpResponse  
from myapp.functions import handle_uploaded_file  
from myapp.forms import Car_Detail,Users
from myapp.models import Car_details,User,Deliveryandreturn,Feedbacks
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import random




# Create your views here.
def admina(request):
    try:
        if request.session['aid']!=None:    
            if request.method=='POST':
                fnam=request.POST['fnam']
                lnam=request.POST['lnam']
                unam=request.POST['usrr']
                mail=request.POST['mail']
                pssc=request.POST['passwo']
                typ=request.POST['type']
                User.objects.create_user(first_name=fnam,last_name=lnam,email=mail,password=pssc,username=unam,type=typ)

                return HttpResponse("Staff added successfuly <a href='/adminhome'><button>Back</button></a>")
            else:
                
                return render(request,'admin.html')
    except:
        messages.add_message(request, messages.INFO, 'Please Login Again.')
        return redirect(logins)



def adminhome(request):
    cars = Car_details.objects.all()
    return render(request,'admin_home.html',{'form':cars})

def add_car(request):  
    try:
        try:   
            if request.session['sid']!= None :
                if request.method == 'POST':  
                    Add_Car = Car_Detail(request.POST, request.FILES)  
                    if Add_Car.is_valid():  
                        Add_Car.save()
                        handle_uploaded_file(request.FILES['c_img'])  
                        return HttpResponse("File uploaded successfuly <a href='/addcar'><button>Back</button></a>")  
                else:  
                    car_table = Car_Detail()  
                    return render(request,"addcar.html",{'form':car_table})
        except:
            if request.session['aid']!= None:
                if request.method == 'POST':  
                    Add_Car = Car_Detail(request.POST, request.FILES)  
                    if Add_Car.is_valid():  
                        Add_Car.save()
                        handle_uploaded_file(request.FILES['c_img'])  
                        return HttpResponse("File uploaded successfuly <a href='/addcar'><button>Back</button></a>")  
                else:  
                    car_table = Car_Detail()  
                    return render(request,"addcar.html",{'form':car_table})

    except:
        messages.add_message(request, messages.INFO, 'Please Login Again.')
        return redirect(logins)

def home(request):
    try :
        if request.session['cid']:
            cid=request.session['cid']
            usr=User.objects.filter(id=cid).get()
            cars = Car_details.objects.all()
            return render(request,'userloging.html',{'form':cars,'usr':usr})
    except:
        cars = Car_details.objects.all()
        return render(request,'index.html',{'form':cars})



def edit(request,id):
    if request.method == 'POST':  
         cname=request.POST['cn']
         cprice=request.POST['cp']
         cdeatil=request.POST['cd']
         Car_details.objects.filter(id=id).update(c_name=cname,c_price=cprice,c_details=cdeatil)
         return redirect(showcars)
    else:
        car_table = Car_details.objects.filter(id=id).get()
        return render(request,"edit.html",{'data':car_table})

            
def showcars(request):
    try:
        try:    
            if request.session['sid']!= None:
                car_table = Car_details.objects.all()  
                return render(request,"editcar.html",{'form':car_table})
        except:
            if request.session['aid']!= None:
                car_table = Car_details.objects.all()  
                return render(request,"editcar.html",{'form':car_table})
    except:
        messages.add_message(request, messages.INFO, 'Please Login Again.')
        return redirect(logins)
def delcar(request,id):
    user=Car_details.objects.filter(id=id).get()
    user.delete()
    return redirect(edit)

def staff(request):
    try:
        if request.session['sid']!= None:
            cars = Car_details.objects.all()
            return render(request,'staf.html',{'form':cars})
        
    except:    
        messages.add_message(request, messages.SUCCESS, 'Please Login Again.')
        return redirect(logins)


def register(request):
    if request.method=='POST':
        fnam=request.POST['first_name']
        lnam=request.POST['last_name']
        usnam=request.POST['username']
        eml=request.POST['email']
        pss=request.POST['password']
        pssc=request.POST['password_confirmation']
        if pss==pssc:
            User.objects.create_user(first_name=fnam,last_name=lnam,email=eml,password=pss,username=usnam,type=3)
            usr=authenticate(request,username=eml,password=pss)
            if usr is not None:
                request.session['cid']=usr.id
                login(request,usr)
                return render(request,'userloging.html',{'usr':usr})
        else:
            messages.add_message(request, messages.INFO, 'Password Does Not Match.')
            return render(request, 'register.html')

    
    else:    
        return render(request,'register.html')

def logins(request,token):

    if request.method=='POST':
        usr=request.POST['user']
        pss=request.POST['passw']
        user=authenticate(request,username=usr,password=pss)

        if user is not None and user.type==3:
            request.session['cid']=user.id
            login(request,user)
            if token==9001:
                cars = Car_details.objects.all()
                return render(request,'userloging.html',{'usr':user,'form':cars})
            elif token==9002:
                return redirect(carsdef)
            elif token==9003:
                return redirect(home)
            
            else:
                cid=request.session['cid']
                usr=User.objects.filter(id=cid).get()
                car=Car_details.objects.filter(id=token).get()
                cars = Car_details.objects.all()
                return render(request,'booknow.html',{'data':car,'form':cars,'usr':usr})

        
        

        elif user is not None and user.type==2:
            request.session['sid']=user.id
            login(request,user)
            return redirect(staff)
        

        elif user is not None and user.type==1:
            request.session['aid']=user.id
            login(request,user)
            return redirect(adminhome)
        else:
            data={'usr':usr,'pss':pss}
            messages.add_message(request, messages.SUCCESS, 'Incorrect Login Credentials')
            return render(request,'login.html',{'dat':data})
    else:
        return render(request,'login.html')

def profile(request):
    cid=request.session['cid']
    usr=User.objects.filter(id=cid).get()
    return render(request,'profile.html',{'usr':usr})

def editprofile(request):
    cid=request.session['cid']
    if request.method=='POST':
        fnam=request.POST['fnam']
        lnam=request.POST['lnam']
        mail=request.POST['mail']
        phone=request.POST['phone']
        User.objects.filter(id=cid).update(first_name=fnam,last_name=lnam,email=mail,phone=phone)
        usr=User.objects.filter(id=cid).get()
        messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
        return render(request,'profile.html',{'usr':usr})

    else:
        usr=User.objects.filter(id=cid).get()
        return render(request,'editprofile.html',{'usr':usr})

def changepass(request):
    cid=request.session['cid']
    if request.method=='POST':
        usr=User.objects.filter(id=cid).get()
        oldps=request.POST['oldpass']
        newps=request.POST['newpas']
        newpss=request.POST['newpass']
        if newps==newpss:
            if usr.check_password(oldps):
                usr.password=make_password(newps)
                
                usr.save()
                messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')

                return redirect(profile)
            else:
                msg={'msg':'Current Password Is Incorrect','value':1}
                return render(request,'changepass.html',{'msgs':msg})
        else:
            msg={'msg':'New Password Not Same','value':2}
            return render(request,'changepass.html',{'msgs':msg})
    else:

        return render(request,'changepass.html')



def carsdef(request):
    try:
        if request.session['cid']:
            cars = Car_details.objects.all()
            cid=request.session['cid']
            usr=User.objects.filter(id=cid).get()
            return render(request,'cars.html',{'form':cars,'usr':usr})    
    except:        
        cars = Car_details.objects.all()
        return render(request,'cars.html',{'form':cars})

def booknow(request,id):
    try:
        if request.session['cid']:
            cid=request.session['cid']
            usr=User.objects.filter(id=cid).get()
            car=Car_details.objects.filter(id=id).get()
            cars = Car_details.objects.all()
            return render(request,'booknow.html',{'data':car,'form':cars,'usr':usr})  
    except:  
        car=Car_details.objects.filter(id=id).get()
        cars = Car_details.objects.all()
        return render(request,'booknow.html',{'data':car,'form':cars})

def booking(request,id):
    try:
        if request.session['cid']:
            if request.method=='POST':
                cid=request.session['cid']
                delivery_place=request.POST['dplace']
                return_place=request.POST['rplace']
                from_date=request.POST['fdate']
                to_date=request.POST['tdate']
                license=request.POST['license']
                Deliveryandreturn.objects.create(cid=cid,dplace=delivery_place,rplace=return_place,rcarid=id,fdate=from_date,rdate=to_date,license=license)
                usrr=User.objects.filter(id=cid).get()
                carss=Car_details.objects.all()
                messages.add_message(request, messages.SUCCESS, 'Booking Success')
                return render(request,'userloging.html',{'usr':usrr,'form':carss})

            else:
                cid=request.session['cid']
                usr=User.objects.filter(id=cid).get()
                car=Car_details.objects.filter(id=id).get()
                return render(request,'booking.html',{'data':car,'usr':usr})
    
    except:
        messages.add_message(request, messages.SUCCESS, 'Please Login To Rent Car.')
        idd={'id':id}
        return render(request,'dlog.html',{'id':idd})
    

def dlog(request,id):
    usr=request.POST['user']
    pss=request.POST['passw']
    user=authenticate(request,username=usr,password=pss)
    if user is not None and user.type==3:
        request.session['cid']=user.id
        login(request,user)
        cid=request.session['cid']
        usr=User.objects.filter(id=cid).get()
        car=Car_details.objects.filter(id=id).get()
        cars = Car_details.objects.all()
        return render(request,'booknow.html',{'data':car,'form':cars,'usr':usr})

        
        

    elif user is not None and user.type==2:
        request.session['sid']=user.id
        login(request,user)
        return redirect(staff)
        

    elif user is not None and user.type==1:
        request.session['aid']=user.id
        login(request,user)
        return redirect(adminhome)
    else:
        data={'usr':usr,'pss':pss}
        messages.add_message(request, messages.SUCCESS, 'Incorrect Login Credentials')
        return render(request,'login.html',{'dat':data})







# def snout(request):
def logout_view(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER', 'default_url'))
    # Redirect to the previous page if available, or a default URL
    # logout(request)
    cars = Car_details.objects.all()
    messages.add_message(request, messages.SUCCESS, 'Logged Out Successfully')
    return render(request,'index.html',{'form':cars})


def corder(request):
    try:
        cid=request.session['cid']
        orders=Deliveryandreturn.objects.filter(cid=cid).all()
        usr=User.objects.filter(id=cid).get()



        a=[]
        for i in orders:
            a.append(i.rcarid)
        print(a)
        cars = Car_details.objects.all()    
        
        return render(request,'orders.html',{'orders':orders,'cars':cars,'booked':a,'usr':usr})
    except:
        return redirect(home)
    
def deleted(request,j):
    dlt=Deliveryandreturn.objects.filter(rcarid=j).get()
    dlt.delete()
    return redirect(corder)

def orders(request):
    orders=Deliveryandreturn.objects.all()

    for order in orders:
        pass
    return render(request,'bookings.html',{'data':orders})

def delreason(request,id):
    if request.method=='POST':
        cid=Deliveryandreturn.objects.filter(rcarid=id).get()
        usr=User.objects.filter(id=cid.cid).get()
        title=request.POST['title']
        msg=request.POST['msg']
        to=request.POST['to']
        res=send_mail(title,msg,'safarjkhan1@gmail.com',[to])
        if res ==1:
            delord=Deliveryandreturn.objects.filter(rcarid=id).get()
            delord.delete()
            return HttpResponse('Mail Sent Success<br><button><a href="/bookings">Back</a></button>')
        else:
            return HttpResponse('Mail Sent Failed<br><button><a href="/bookings">Back</a></button>')
    else:
        cid=Deliveryandreturn.objects.filter(rcarid=id).get()
        usr=User.objects.filter(id=cid.cid).get()
        return render(request,'reasondel.html',{'usr':usr})
    
def passreset(request):
    cd=request.POST['usorem']
    try:
        usr=User.objects.filter(username=cd).get()
        if usr:
            otp=random.randint(1111,9999)
            res=send_mail('Password Reset OTP',otp,'safarjkhan1@gmail.com',[usr.email])
        else:
            return HttpResponse('Hiiii')
    except:
        return HttpResponse('byeee')
          

def feedbak(request):
    name=request.POST['name']
    desc=request.POST['describ']
    Feedbacks.objects.create(name=name,describe=desc)
    return redirect(home)


def stffeedback(request):
    fbs=Feedbacks.objects.all()
    return render(request,'staffbsview.html',{'data':fbs})
