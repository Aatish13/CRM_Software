from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignUpForm
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from accounts.models import UserType
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def home(request):
	return render_to_response('home.html')


# class SignUp(generic.CreateView):
#     form_class = SignUpForm
#     success_url = reverse_lazy('home/')
#     template_name = 'signup.html'

@login_required(login_url = '/accounts/login/')
def changePass(request):
	return render(request,'changePass.html')
@login_required(login_url = '/accounts/login/')
def processChange(request):
	if request.method=='POST':
		id=request.user.id
		user_obj=User.objects.get(id=id)
		old_pass=request.POST.get('old','')
		user = authenticate(username=user_obj.username, password=old_pass)
		if user is not None:
			new_pass = request.POST.get('pwd1', '')
			user_obj.set_password(new_pass)
			user_obj.save()
			#print("NEW PASSWORD"+new_pass)
			#print("OLD PASSWORD"+old_pass)
		return HttpResponseRedirect('/manager/dashboard')


def register (request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			user_type = request.POST.get('user_type','')
			user_name = request.POST.get('username', '')
			print(user_type)
			form.save()

			t = User.objects.get(username=user_name)
			u = UserType.objects.get(user_id=t.id)
			u.user_type=user_type
			u.user_name=user_name
			u.save()
			return render_to_response('login.html',{"username":user_name,"password":request.POST.get('password', '')})
	else:
		form = SignUpForm()
	args = {'form': form}
	return render(request, 'signup.html', args)


@login_required(login_url = '/accounts/login/')
def changePass(request):
	return render_to_response('changePass.html')
@login_required(login_url = '/accounts/login/')
def processChange(request):
	if request.method=='POST':
		id=request.user.id
		user_obj=User.objects.get(id=id)
		old_pass=request.POST.get('old','')
		user = authenticate(username=user_obj.username, password=old_pass)
		if user is not None:
			new_pass = request.POST.get('pwd1', '')
			user_obj.set_password(new_pass)
			user_obj.save()
			#print("NEW PASSWORD"+new_pass)
			#print("OLD PASSWORD"+old_pass)
		return HttpResponseRedirect('/manager/dashboard')






def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

@login_required(login_url = '/accounts/login/')
def info(request):
	uid=User.objects.get(id=request.user.id)
	return render_to_response('accountdetails.html',{"user":uid})


@login_required(login_url = '/accounts/login/')
def delete(request):
	acno = request.POST.get("empid", '')
	uid = User.objects.get(id=acno)
	return render_to_response('confirmation.html',{"user":uid})




@login_required(login_url = '/accounts/login/')
def viewProfile(request):
	acno=request.POST.get("empid",'')
	uid=User.objects.get(id=acno)
	print(uid)
	return render(request,'viewinfo.html',{"employee":uid})

@login_required(login_url = '/accounts/login/')
def update(request):
	if request.method == 'GET':
		u=User.objects.get(id=request.user.id)
		u.first_name=request.GET.get('first_name','')
		u.last_name = request.GET.get('last_name', '')
		u.email = request.GET.get('email', '')
		u.save()
	return render(request,'accountdetails.html')

@login_required(login_url = '/accounts/login/')
def loggedin(request):
	if request.user.is_authenticated:
		return render_to_response('loggedin.html', {"full_name": request.user.username})
	else:
		return HttpResponseRedirect('/login/login/')

def invalidlogin(request):
	return render_to_response('invalidlogin.html')


def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	print(user)
	if user is not None:
		auth.login(request,user)
		u = UserType.objects.filter(user_name=username)
		request.session['user_type'] = u[0].user_type
		if u[0].user_type=='manager':
			return HttpResponseRedirect('/manager/dashboard')
		elif u[0].user_type=='employee':
			return HttpResponseRedirect('/employee/dashboard?username='+str(u[0].user_name))
		elif u[0].user_type=='customer':
			return render_to_response('loggedin.html', {'user': u})
		else:
			return render_to_response('errorpage.html', {'user': u})
	else:
		return HttpResponseRedirect('/accounts/invalidlogin/')


def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')
# Create your views here.
