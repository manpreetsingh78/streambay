# from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate, Reset, Replacement
import json
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
# import requests
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf

# from PayTm import Checksum
# MERCHANT_KEY= 'fHJgrS3&0myFfK6g'
# Create your views here.

def home(request):
    products= Product.objects.all()
    print(products)
    params = {
        'product':products
    }
    
    return render(request, 'shop/home.html',params)

# def checkout(request):
#     return render(request, 'shop/checkout.html')

def about(request):
    return render(request, 'shop/about.html')

# def video(request):
#     return render(request, 'shop/video.html')

def contact(request):
    thank = False
    if request.method=="POST":
        # name = request.POST.get('name', '')
        name = request.POST.get('firstName', '') + " " + request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html/', {'thank': thank})

def replacement(request):
    # return render(request,'shop/replacement.html')
    thank = False
    if request.method=="POST":
        # name = request.POST.get('name', '')
        name = request.POST.get('firstName', '') + " " + request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        # order_id = request.POST.get('order_id', '')
        orderx = request.POST.get('order_id','')
        # order_id = int(request.POST.get('order_id', '')[7:])
        order_id = int(orderx[6:])

        product_name = request.POST.get('product_name', '')
        product_email = request.POST.get('product_email', '')
        password = request.POST.get('password', '')
        desc = request.POST.get('desc', '')
        replacement = Replacement(name=name, email=email, phone=phone, order_id=order_id, product_name=product_name, product_email=product_email, password=password, desc=desc)
        replacement.save()
        thank = True
    return render(request, 'shop/replacement.html/', {'thank': thank})

def reset(request):
    # return render(request,'shop/replacement.html')
    thank = False
    if request.method=="POST":
        # name = request.POST.get('name', '')
        name = request.POST.get('firstName', '') + " " + request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        orderx = request.POST.get('order_id','')
        # order_id = int(request.POST.get('order_id', '')[7:])
        order_id = int(orderx[6:])

        product_name = request.POST.get('product_name', '')
        product_email = request.POST.get('product_email', '')
        password = request.POST.get('password', '')
        desc = request.POST.get('desc', '')
        reset = Reset(name=name, email=email, phone=phone, order_id=order_id, product_name=product_name, product_email=product_email, password=password, desc=desc)
        reset.save()
        thank = True
    return render(request, 'shop/replacement.html/', {'thank': thank})



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    # response = json.dumps(updates, default=str)
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                # return HttpResponse('{}')
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            # return HttpResponse('{}')
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


# def success(request):
#     template = render_to_string('shop/orderEmail.html')
#     email= EmailMessage(
#         'Order Confirmation',
#         template,
#         settings.EMAIL_HOST_USER,
#         [email],
#     )
#     email.fail_silently = False
#     email.send()
#     return render(request,'shop/home.html')


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('firstName', '') + " " + request.POST.get('lastName', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        MERCHANT_KEY = "eCQxpxK3"
        key="eCQxpxK3"
        SALT = "h3gvnlupey"
        PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
        surl = "shop/success.html"
        furl = "shop/failure.html"
        action = ''
        posted={}
        # Merchant Key and Salt provided y the PayU.
        # for i in request.POST:
        #     posted[i]=request.POST[i]
        posted={
            'key':key,
            'amount': float("{:.2f}".format(float(amount))),
            'productinfo': items_json,
            'firstname': name,
            'email' : email,
            'phone': phone,
            'surl': 'http://127.0.0.1:8000/shop/success/',
            'furl': 'http://127.0.0.1:8000/shop/failure/',
            'service_provider': 'payu_paisa',

        }
        hash_object = hashlib.sha256('randint(0,20)'.encode('utf-8'))
        txnid=hash_object.hexdigest()[0:20]
        hashh = ''
        posted['txnid']=str(order.order_id)
        # posted['key']=key
        hashSequence = "key|txnid|amount|productinfo|firstname|email|||||||||||SALT"
        hash_string=''
        hashVarsSeq=hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string+=str(posted[i])
            except Exception:
                hash_string+=''
            hash_string+='|'
        hash_string+=SALT
        hashh=hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        posted['hash']=hashh
        action =PAYU_BASE_URL
        if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
            return render(request,'shop/current_datetime.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://sandboxsecure.payu.in/_payment" })
        else:
            return render(request,'shop/current_datetime.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"." })
        
    return render(request, 'shop/checkout.html')



@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt="h3gvnlupey"
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render_to_response(request,'shop/sucess.html',{"txnid":txnid,"status":status,"amount":amount})


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt="h3gvnlupey"
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render_to_response(request,"shop/Failure.html")

    


 # template = render_to_string('shop/orderEmail.html',{'name':name,'orderId':id,'amount':amount})
        # email = EmailMessage(
        #     'Order Confirmation',
        #     template,
        #     settings.EMAIL_HOST_USER,
        #     [email],
        # )
        # email.fail_silently = False
        # email.send()
    
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
       