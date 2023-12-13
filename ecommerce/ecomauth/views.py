from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def signup(request):
    
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request, 'auth/signup.html')
        try:
            if User.objects.get(username=email):
                messages.warning(request, 'Email is already Taken')
                return render(request, 'auth/signup.html')
        except Exception as identifier:
            pass
        
        myuser = User.objects.create_user(email,email,password)
        myuser.save()
        messages.info(request,"Signup SuccessFull! Please Login")
        return redirect('/ecomauth/login')
    
    return render(request, 'auth/signup.html')


def handlelogin(request):
    if request.method=='POST':
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username,password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request,'Login Success')
            return render(request, 'index.html')
        else:
            messages.error(request, 'Invalid Credentails')
            return redirect('/ecomauth/login/')
        
    return render(request, 'auth/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Sucess")
    return redirect('/ecomauth/login/')