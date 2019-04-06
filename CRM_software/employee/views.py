from django.shortcuts import render
from django.shortcuts import render_to_response
from employee.models import employee,employee_customer
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm
from manager.models import Product
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from accounts.models import UserType
from datetime import datetime

# Create your views here.
@login_required(login_url = '/accounts/login/')
def dashboard(request):
	t=[]
	l1=[]
	data=[0,0,0,0,0,0,0,0,0,0,0,0]
	cdate=datetime.date(datetime.now())
	str2=str(cdate)
	username=request.session.get('username')
	v=User.objects.filter(username=username)
	eid=v[0].id
	flag=employee_customer.objects.filter(e_id=eid).exists()
	if flag:
		#t=employee_customer.objects.filter(e_id=eid)
		t=employee_customer.objects.raw("SELECT COUNT(id) as c,id,r_date FROM `employee_employee_customer` GROUP by month(r_date),year(r_date),e_id HAVING e_id="+str(eid))
		str1=str(t[0].r_date)
		s=int(str1[5:7])
		j=s-1
		data=[0,0,0,0,0,0,0,0,0,0,0,0]
		for i in t:
			str1=i.r_date
			str1=str(str1)
			if str1[:4]==str2[:4]:
				data[j]=i.c
				j=j+1
		tope=employee_customer.objects.raw("SELECT id,COUNT(id) as cou,e_id FROM employee_employee_customer GROUP BY e_id  ORDER BY cou DESC")
		i=0
		for k in tope:
			l=[]
			print(k.e_id)
			ed=User.objects.filter(id=k.e_id)
			l.append(ed)
			l.append(k.cou)
			l1.append(l)
			i+=1
			if i>4:
				break
		print(l1)
	#print(data)
	arg={'data':data,'user':v[0],'list':l1}
	return render(request,'empdashboard.html',arg)

@login_required(login_url = '/accounts/login/')
def customer(request):
	username=request.session.get('username')
	ob=User.objects.filter(username=username)
	ecob=employee_customer.objects.filter(e_id=ob[0].id)
	arg={'ob':ecob,'user':ob[0]}
	return render(request,'customer.html',arg)

@login_required(login_url = '/accounts/login/')
def register(request):
	#print(request.session.get('username'))
	e_username=request.session.get('username')
	ob=User.objects.filter(username=e_username)
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			user_type = 'customer'
			user_name = request.POST.get('username', '')
			print(user_type)
			form.save()

			t = User.objects.get(username=user_name)
			u = UserType.objects.get(user_id=t.id)
			u.user_type=user_type
			u.user_name=user_name
			u.save()
		eob=User.objects.get(username=e_username)
		pob=Product.objects.get(name=request.POST.get('s_product',''))
		c=employee_customer(c_name=request.POST.get('username',''))
		c.e_id=eob.id
		c.product_id=pob.id
		c.save()
		return HttpResponseRedirect('/employee/dashboard')
	else:
		form=SignUpForm()
		p=Product.objects.all()
		arg={'form':form,'pro':p,'user':ob[0]}
		return render(request,'register.html',arg)

@login_required(login_url = '/accounts/login/')
def totalsale(request):
	if request.POST.get("empid",''):
		acno=request.POST.get("empid",'')
		e_username=User.objects.get(id=acno)
	else:
		e_username=request.session.get('username')
	eob=User.objects.get(username=e_username)
	cdate=datetime.date(datetime.now())
	str2=str(cdate)
	l=[0,0,0,0,0,0,0,0,0,0,0,0]
	ly=[0,0,0,0,0,0,0]
	t=employee_customer.objects.raw("SELECT employee_employee_customer.id,SUM(manager_product.price) as sum,r_date from employee_employee_customer,manager_product WHERE product_id=manager_product.id and e_id=\'"+str(eob.id)+'\''+" GROUP BY month(r_date),year(r_date)")
	str1=str(t[0].r_date)
	s=int(str1[5:7])
	j=s-1
	for i in t:
		str1=i.r_date
		str1=str(str1)
		if str1[:4]==str2[:4]:
			l[j]=i.sum
			j=j+1
	t=employee_customer.objects.raw("SELECT employee_employee_customer.id,SUM(manager_product.price) as sum,r_date from employee_employee_customer,manager_product WHERE product_id=manager_product.id and e_id=\'"+str(eob.id)+'\''+" GROUP BY year(r_date)")
	str1=str(t[0].r_date)
	s=int(str1[:4])
	j=s-2019
	for i in t:
		ly[j]=i.sum
		j=j+1

	arg={'slist':l,'ylist':ly,'user':eob}
	return render(request,'totalsale.html',arg)

@login_required(login_url = '/accounts/login/')
def existing(request):
	if request.method=='POST':
		eob=User.objects.get(username=request.session.get('username'))
		pob=Product.objects.get(name=request.POST.get('s_product',''))
		c=employee_customer(c_name=request.POST.get('customer',''))
		c.e_id=eob.id
		c.product_id=pob.id
		c.save()
		return HttpResponseRedirect('/employee/dashboard')
	else :
		p=Product.objects.all()
		c=UserType.objects.filter(user_type='customer')
		arg={'pro':p,'cus':c}
		return render(request,'existing.html',arg)
