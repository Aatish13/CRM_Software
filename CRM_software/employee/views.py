from django.shortcuts import render
from django.shortcuts import render_to_response
from employee.models import employee,employee_customer
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm
from manager.models import Product
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from accounts.models import UserType

# Create your views here.
@login_required(login_url = '/accounts/login/')

def dashboard(request):
	a=0
	t=[]
	data=[]
	username=request.GET.get('username','')
	eob=UserType.objects.filter(user_name=username).exists()
	if not eob:
		e_instance = employee.objects.create(e_name=username)
		data=[0,0,0,0,0,0,0,0,0,0,0,0]
	else:
		v=User.objects.filter(username=username)
		eid=v[0].id
		#t=employee_customer.objects.filter(e_id=eid)
		#t=employee_customer.objects.raw("SELECT COUNT(id) as c,id,r_date FROM `employee_employee_customer` GROUP by month(r_date),e_id HAVING e_id="+str(eid))
		#str1=str(t[0].r_date)
		#s=int(str1[5:7])
		#j=s-1
		data=[0,0,0,0,0,0,0,0,0,0,0,0]
		#for i in t:
		#	data[j]=i.c
		#	j=j+1
		#print(data)
	arg={'username':request.GET.get('username',''),'count':a,'data':data}
	return render_to_response('empdashboard.html',arg)

def customer(request):
	username=request.GET.get('username','')
	ob=employee.objects.filter(e_name=username)
	ecob=employee_customer.objects.filter(e_id=ob[0].id)
	arg={'ob':ecob,'username':username}
	return render(request,'customer.html',arg)

def register(request):
	e_username=request.GET.get('username','')
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
		arg={'username':e_username}
		return HttpResponseRedirect('/employee/dashboard?username='+str(e_username))
	else:
		form=SignUpForm()
		p=Product.objects.all()
		arg={'form':form,'username':e_username,'pro':p}
		return render_to_response('register.html',arg)