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

#Geting Tokens from Utils
from .utils import generate_token
from .utils import TokenGenerator

#emails
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
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
        # myuser.is_active=False
        myuser.save()
        # current_site = get_current_site(request)
        # #activate account
        # email_subject = "Activate your Account"
        # message = render_to_string('auth/activate.html',{
        #     'user': myuser,
        #     'domain': '127.0.0.1:8000',
        #     'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        # })
        # #sent a message
        # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        # EmailThread(email_message).start()
        # messages.info(request,"Activate Your Account by clicking link on your email")
        messages.info(request,"Registeration Successfully")
        return redirect('/ecomauth/login')
    
    return render(request, 'auth/signup.html')


class ActivateAccountView(View):
    def get(self, request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/ecomauth/login')
        
        return render(request, 'auth/activate_fail.html')
            
            
            
    

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