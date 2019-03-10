from django.shortcuts import render
from manager.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from accounts.models import UserType
from django.core.mail import send_mail
from employee.models import employee_customer
# Create your views here.


@login_required(login_url = '/accounts/login/')
def dashboard(request):
    if request.session['user_type']=='manager':
        sales = employee_customer.objects.all()
        for sal in sales:
            print(sal.c_name,sal.product.price,sal.r_date.month,sal.r_date.year)
        #t = employee_customer.objects.raw(
         #   "SELECT COUNT(id) as c,id,r_date FROM `employee_employee_customer` GROUP by month(r_date),e_id ")
        data = [299, 3000, 2000, 1000, 1111, 111,2222, 5499,2222]
        return render(request,'mandashboard.html',{"data":data,"sales":sales})
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def display_employees(request):
    if request.session['user_type'] == 'manager':
        e = UserType.objects.filter(user_type="employee")
        employee=set()
        for emp in e:
            u= User.objects.filter(id=emp.user_id)
            employee=set(employee).union(set(u))
        print(employee)
        sales= employee_customer.objects.all()
        return render(request,'viewemp.html',{"employee_list":employee ,"sales_list":sales})
    else:
        message = "Login in as manager to access this page."
        return render(request, 'error.html', {'message': message})

@login_required(login_url = '/accounts/login/')
def display_customers(request):
    if request.session['user_type'] == 'manager':
        c = UserType.objects.filter(user_type="customer")
        customers = set()
        for cus in c:
            u= User.objects.filter(id=cus.user_id)
            customers=set(customers).union(set(u))
        print(customers)
        return render(request, 'viewcust.html', {"customers_list":customers} )
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def display_products(request):
    if request.session['user_type'] == 'manager':
        p=Product.objects.all()
        return render(request, 'viewprod.html', {"product_list":p} )
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def register_product(request):
    if request.session['user_type'] == 'manager':
        if request.method=='POST':
            pname=request.POST.get('pname','')
            pprice=request.POST.get('price','')
            pdescription=request.POST.get('description','')
            print(pname,pprice,pdescription)
            p=Product(name=pname,price=pprice,description=pdescription)
            p.save()
           # send_mail('Testing mail'+pname, 'This is an auto generated mail product added'+pname, 'adchaudhari70@outlook.com', ['adchaudhari70.ac@gmail.com'],fail_silently=False)
        return render(request, 'productform.html')
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})