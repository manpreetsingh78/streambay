from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate, Reset, Replacement
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import razorpay

client = razorpay.Client(auth=("rzp_test_Vhi7uERAcssGSC", "Jxcnk0LCwIHZ4D4ZwjfdPriU"))
# client = razorpay.Client(auth=("rzp_live_wkPKQnPOP7FNhi", "GXHoH0vED6vR0L5Zua0MAy0g"))

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
        oid = request.POST.get('order_id','')
        # order_id = int(request.POST.get('order_id', '')[7:])
        # order_id = int(orderx[6:])

        product_name = request.POST.get('product_name', '')
        product_email = request.POST.get('product_email', '')
        password = request.POST.get('password', '')
        desc = request.POST.get('desc', '')
        replacement = Replacement(name=name, email=email, phone=phone, oid=oid, product_name=product_name, product_email=product_email, password=password, desc=desc, order_id="0")
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
        oid = request.POST.get('order_id','')
        # order_id = int(request.POST.get('order_id', '')[7:])
        # order_id = int(orderx[6:])

        product_name = request.POST.get('product_name', '')
        product_email = request.POST.get('product_email', '')
        password = request.POST.get('password', '')
        desc = request.POST.get('desc', '')
        reset = Reset(name=name, email=email, phone=phone, oid=oid, product_name=product_name, product_email=product_email, password=password, desc=desc)
        reset.save()
        thank = True
    return render(request, 'shop/replacement.html/', {'thank': thank})



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(oid=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(oid=orderId)
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
        thank = True
        
        context = {}
        
        order_amount1 = int(amount)* 100
        order_amount = order_amount1   
        # order_amount = amount       
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        
        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
        order_id = response['id']
        order_status = response['status']
        print(order_id)
        if order_status=='created':
            order = Orders(items_json=items_json, name=name, email=email, phone=phone, amount=amount, oid=order_id)
            order.save()
            update = OrderUpdate(order_id=order.order_id,oid=order.oid, update_desc="The order has been placed")
            update.save()
            # Server data for user convinience
            context['product_id'] = items_json
            context['price'] = order_amount
            context['name'] = name
            context['phone'] = phone
            context['email'] = email

            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            

            return render(request, 'shop/confirm_order.html', context)
        return render(request,'shop/order_failure.html')
    return render(request, 'shop/checkout.html')


def payment_status(request):

    response = request.POST
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature'], 
    }


    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        print(status)
        print(status)
        order = Orders.objects.filter(oid= params_dict['razorpay_order_id'])
        # order = Orders.objects.filter(order_id = response['razorpay_order_id'])
        for item in order:
            name=item.name
            emailId= item.email
            amount =item.amount
            order_id =item.order_id
            oid = item.oid
        ord = OrderUpdate.objects.filter(order_id=order_id)
        if len(ord)==1:
            template = render_to_string('shop/orderEmail.html',{'params_dict':params_dict,'name':name, 'amount':amount})
            email= EmailMessage(
                'Order Confirmation',
                template,
                settings.EMAIL_HOST_USER,
                [emailId],
            )
            email.fail_silently = False
            email.send()
            update = OrderUpdate(order_id=order_id,oid=oid, update_desc="The payment has been confirmed.")
            update.save()
        return render(request, 'shop/order_success.html', {'status': 'Payment Successful','params_dict':params_dict,'email':emailId})
    # except:
    #     return render(request, 'shop/order_failure.html', {'status': 'Payment Faliure!!!'})
    except Exception as e: 
        print(e)
        return HttpResponse("Errrroooee")