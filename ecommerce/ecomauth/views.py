from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
#activate user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
# from django.utils.encoding import force_text
from django.utils.encoding import force_str
from django.http import HttpResponse
#Geting Tokens from Utils
from .utils import generate_token
from .utils import TokenGenerator

# restpassword generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
#emails
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
#threading
import threading
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        # Threading.Thread.__init__(self)
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

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
        myuser.is_active=False
        myuser.save()
        current_site = get_current_site(request)
        #activate account
        email_subject = "Activate Link has been sent to your email id"
        message = render_to_string('auth/activate.html',{
            'user': myuser,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            # 'token': generate_token.make_token(myuser)
            'token': generate_token.make_token(myuser)
        })
        # to_email = form.cleaned_data.get('email')
        
        #sent a message
        # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        email_message = EmailMessage(email_subject,message,to=[email])
        email_message.send()
        EmailThread(email_message).start()
        messages.info(request,"Activate Your Account by clicking link on your email")
        # messages.info(request,"Registeration Successfully")
        return redirect('/ecomauth/login')
    
    return render(request, 'auth/signup.html')


# class ActivateAccountView(View):
#     def get(self, request,uidb64,token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None
        
#         if user is not None and generate_token.check_token(user,token):
#             user.is_active=True
#             user.save()
#             messages.info(request,"Account Activated Successfully")
#             return redirect('/ecomauth/login')
        
#         return render(request, 'auth/activate_fail.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        return HttpResponse('Thank you for your confirmation. Now you can login to your account')
    else:
        return HttpResponse('Activation link is invalid')
             
            
            
    

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


class RequestResetEmail(View):
    def get(self, request):
        return render(request, 'auth/request-rest.html')
    
    def post(self, request):
        email = request.POST['email']
        user =  User.objects.filter(email=email)
        
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset Your Password]'
            message = render_to_string('auth/rest-user-password.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token':  PasswordResetTokenGenerator().make_token(user[0])
                                       })
            
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            
            EmailThread(email_message).start()
            
            messages.info(request,"We have sent you an email for reset password")
            return render(request,'auth/request-rest.html')
        
class SetNewPasswordView(View):
    
    def get(self,request, uidb64,token):
        context = {
            'uidb64':uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password reset link is Invalid")
                return render(request,'auth/request-rest.html',context)
        except DjangoUnicodeDecodeError as identifier:
            pass
        
        return render(request,'auth/set-new-password.html',context)
    
    def post(self, request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request, 'auth/set-new-password.html',context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset Sucees Please Login")
            return redirect ('/ecomauth/login/')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request," Something went wrong") 
            return render (request,'auth/set-new-password.html',context)
        return render (request,'auth/set-new-password.html',context)
        