from django.shortcuts import render
from django.http import HttpResponse
from .models import Product , Contact , Order , OrderUpdate
from math import ceil
from django.views import generic
import json
from django.views.decorators.csrf import csrf_exempt
import razorpay
def index(request):
    allProds = []
    catprods = Product.objects.values('category' , 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats :
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
        params = {'allProds':allProds}
    return render(request,'shop/index.html', params)

def searchMatch(query, item):
    
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
            params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        PhoneNo=request.POST.get('PhoneNo','')
        message =request.POST.get('message','')
        contact = Contact(name = name , email = email, PhoneNo = PhoneNo, message = message)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
      if request.method == "POST":
        orderID = request.POST.get('orderId','')
        email = request.POST.get('email','')
        
        try:
            order = Order.objects.filter(order_id=orderId, email= email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
            
      return render(request,'shop/tracker.html')


def products(request, myid):
    #fetch the product using the id
     product = Product.objects.filter(id=myid)

     return render(request,'shop/ProductView.html', {'product':product[0]})

# def checkout(request):
#      return render(request,'shop/checkout.html')

# def checkout(request):
#     if request.method=="POST":
#         items_json  = request.POST.get('itemsJson', '')
#         name=request.POST.get('name', '')
#         email=request.POST.get('email', '')
#         address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city=request.POST.get('city', '')
#         state=request.POST.get('state', '')
#         zip_code=request.POST.get('zip_code', '')
#         phone=request.POST.get('phone', '')

#         Order=Order(items_json  = items_json , name=name, email=email, address= address, city = city,     state=state, zip_code=zip_code, phone=phone)
#         Order.save()
#         thank = True
#         id = Order.Order_id
#         return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
#     return render(request, 'shop/checkout.html')

razorpay_client = razorpay.Client(auth=('RAZORPAY_API_KEY', 'RAZORPAY_SECRET_KEY'))

def checkout(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone = request.POST['phone']
        items_json = request.POST['itemsJson']
        amount = float(request.POST['amount']) * 100  # Amount in paise for Razorpay

        # Create an Order object
        order = Order(
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            items_json=items_json,
            amount=amount / 100,  # Store in rupees
        )
        order.save()

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(
            {"amount": amount, "currency": "INR", "payment_capture": "1"}
        )
        order.order_id = razorpay_order['id']
        order.save()

        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': 'RAZORPAY_API_KEY',
            'amount': amount,
            'currency': 'INR',
        }
        return render(request, 'shop/payment.html', context)
    return render(request, 'shop/checkout.html', {"error": "Invalid request method."})
@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        response = request.POST
        params_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature')
        }

        # Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(order_id=response.get('razorpay_order_id'))
            order.payment_id = response.get('razorpay_payment_id')
            order.paid = True
            order.save()
            return render(request, 'shop/paymentstatus.html', {'order': order})
        except razorpay.errors.SignatureVerificationError:
            return render(request, 'shop/checkout.html')
def cart(request):
    return render(request,'shop/cart.html')
