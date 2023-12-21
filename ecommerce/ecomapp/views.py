from django.shortcuts import render, redirect
from . models import Product,Orders,OrderUpdate
from math import ceil
from ecomapp import key
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'index.html')

def Purchase(request):
    current_user = request.user
    print(current_user)
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        
        
    params = {'allProds': allProds}
    return render(request,'purchase.html', params)

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Again")
        return redirect('/ecomauth/login')
    
    if request.method=="POST":
        
        itemn_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amt')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1','')
        address2  = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')  
        phone = request.POST.get('phone','') 
        
        
        order = Orders(itemn_json=itemn_json, name=name, amount=amount,email=email,address1=address1,address2=address2,
                       city=city,state=state,zip_code=zip_code,
                       phone=phone) 
        print(amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        
        #payment intigration
        id = order.order_id
        oid = str(id)+"bodybag"
        param_dict = {
            'MID': 'MID',
            'ORDER'
            
        }
    return render(request, 'checkout.html')   
