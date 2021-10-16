from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate, Reset, Replacement
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from PayTm import Checksum
MERCHANT_KEY= 'fcZNMtm!Ms1k45hb'
# MERCHANT_KEY= '5LO0BQOd3abbAn9v'
# Create your views here.

def home(request):
    products= Product.objects.all()
    print(products)
    params = {
        'product':products
    }
    
    return render(request, 'shop/home.html',params)

def about(request):
    return render(request, 'shop/about.html')

def terms(request):
    return render(request, 'shop/terms.html')

def privacy(request):
    return render(request, 'shop/privacy.html')

def refund(request):
    return render(request, 'shop/refund.html')

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

        param_dict = {

                # 'MID': 'waLUWl48954879844666',
                # 'ORDER_ID': str(order.order_id),
                # 'TXN_AMOUNT': str(amount),
                # 'CUST_ID': email,
                # 'INDUSTRY_TYPE_ID': 'Retail',
                # 'WEBSITE': 'DEFAULT',
                # 'CHANNEL_ID': 'WEB',
                # 'CALLBACK_URL':'http://127.0.0.1:8000/shop/orderstatus/',

                'MID': 'iqgxNE34734651948434',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://streambay.net/shop/orderstatus/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
 
    return render(request, 'shop/checkout.html')

def addcoupon(request):
    return render(request, 'shop/checkout .html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            order = Orders.objects.filter(order_id = response_dict['ORDERID'])
            for item in order:
                name=item.name
                emailId= item.email
            template = render_to_string('shop/orderEmail.html',{'response_dict':response_dict,'name':name})
            email= EmailMessage(
                'Order Confirmation',
                template,
                settings.EMAIL_HOST_USER,
                [emailId],
            )
            email.fail_silently = False
            email.send()
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            emailId=''
    return render(request, 'shop/paymentstatus.html', {'response': response_dict,'email':emailId})

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
       