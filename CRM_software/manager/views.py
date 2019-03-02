from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from accounts.models import UserType

# Create your views here.
@login_required(login_url = '/accounts/login/')
def dashboard(request):
	return render_to_response('mandashboard.html')

def display_employees(request):
	e = UserType.objects.filter(user_type="employee")
	employee=set()
	for emp in e:
		u= User.objects.filter(id=emp.user_id)
		employee=set(employee).union(set(u))
	print(employee)
	return render(request,'viewemp.html',{"employee_list":employee})