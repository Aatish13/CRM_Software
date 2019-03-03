from django.shortcuts import render
from manager.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from accounts.models import UserType
from django.core.mail import send_mail
# Create your views here.
@login_required(login_url = '/accounts/login/')
def dashboard(request):
	return render_to_response('mandashboard.html')


@login_required(login_url = '/accounts/login/')
def display_employees(request):
	e = UserType.objects.filter(user_type="employee")
	employee=set()
	for emp in e:
		u= User.objects.filter(id=emp.user_id)
		employee=set(employee).union(set(u))
	print(employee)
	return render(request,'viewemp.html',{"employee_list":employee})

@login_required(login_url = '/accounts/login/')
def display_customers(request):
	c = UserType.objects.filter(user_type="customer")
	customers = set()
	for cus in c:
		u= User.objects.filter(id=cus.user_id)
		customers=set(customers).union(set(u))
	print(customers)
	return render(request, 'viewcust.html', {"customers_list":customers} )

@login_required(login_url = '/accounts/login/')
def display_products(request):
	p=Product.objects.all()
	return render(request, 'viewprod.html', {"product_list":p} )

@login_required(login_url = '/accounts/login/')
def register_product(request):
	if request.method=='POST':
		pname=request.POST.get('pname','')
		pprice=request.POST.get('price','')
		pdescription=request.POST.get('description','')
		print(pname,pprice,pdescription)
		p=Product(name=pname,price=pprice,description=pdescription)
		p.save()
		send_mail('Testing mail'+pname, 'This is an auto generated mail product added'+pname, 'adchaudhari70@outlook.com', ['adchaudhari70.ac@gmail.com'],fail_silently=False)
	return render(request, 'productform.html')
