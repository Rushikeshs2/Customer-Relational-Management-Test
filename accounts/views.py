from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import *
from .filters import OrderFilter
from .forms import  OrderForm,createUserForm,CustomerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login,logout
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.core.mail import send_mail,send_mass_mail,BadHeaderError
from django.conf import settings
from django import forms
from .utils import get_plot
@unauthenticated_user
def registerpage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    context ={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username= username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
    

    context = {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url ='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customers.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders' : orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)


@login_required(login_url ='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customers.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    if request.method == 'POST':
        email = request.POST['email']
        newsletter = Newsletter(email=email)
        newsletter.save()
    context = {'orders' : orders,'customers' : customers,'total_customers' : total_customers, 'total_orders': total_orders,'delivered':delivered,'pending': pending}
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url ='login')
def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{'products' : products})
@login_required(login_url ='login')
def customer(request, pk_test):
    customer = Customers.objects.get(id = pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs
    context ={'customer': customer,'orders':orders,'order_count':order_count,'myFilter' :myFilter}
    return render(request,'accounts/customer.html',context)
@login_required(login_url ='login')
@allowed_users(allowed_roles=['customer','admin'])
def accountsSettings(request):
	customers = request.user.customers
	form = CustomerForm(instance=customers)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customers)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url ='login')
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customers, Order, fields =('product','status'),extra = 10)
    customer = Customers.objects.get(id=pk)
   # form = OrderForm(initial={'customer': customer})
    formset = OrderFormSet( queryset=Order.objects.none(), instance = customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')



    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)
@login_required(login_url ='login')
@admin_only
def update_order(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        #print('Printing post',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)
@login_required(login_url ='login')
@admin_only
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    context={'item':order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request,'accounts/delete.html',context)
def contactus(request):
    if request.method == 'POST':
         name = request.POST['name']
         email = request.POST['email']
         phone = request.POST['phone']
         content = request.POST['content']
         if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)< 3 :
             messages.error(request,'Please fil the form correctly')
         else:
             contact = Contact(name=name,email=email,phone=phone,content=content)
             contact.save()
             message1 = (name + '  submitted contact form' , 'his phone no.- ' + phone + ' his email- '+ email + ' message from him - ' + content ,'susarrushi@gmail.com',
              ['rspatil0103@gmail.com'])
             message2 = ( 'We Welcome you to CRM. ',
                'You will recieve our call shortly.',
                 'rspatil0103@gmail.com',
                 [email],)
             send_mass_mail((message1,message2),fail_silently=False)
             messages.success(request,'form filled  correctly')
    return render(request,'accounts/contact.html')

@login_required(login_url ='login')
@admin_only
def matplot(request):
	qs = Product.objects.all()
	x = [x.name for x in qs]
	y = [y.price for y in qs]
	chart = get_plot(x,y)
	return render(request, 'accounts/matplot.html',{'chart':chart})