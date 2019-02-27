from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from loginModule.forms import SignUpForm
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from loginModule.models import UserType
from django.contrib import auth
from django.http import HttpResponseRedirect
def home(request):
	return render_to_response('home.html')


# class SignUp(generic.CreateView):
#     form_class = SignUpForm
#     success_url = reverse_lazy('home/')
#     template_name = 'signup.html'


def register (request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			user_type = request.POST.get('user_type','')
			user_name = request.POST.get('username', '')
			print(user_name,user_type)
			form.save()
			u = UserType(user_type=user_type,user_name=user_name)
			u.save()
			return render(request,'login.html')
	else:
		form = SignUpForm()
	args = {'form': form}
	return render(request, 'signup.html', args)

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

@login_required(login_url = '/login/login/')
def loggedin(request):
	if request.user.is_authenticated:
		return render_to_response('loggedin.html', {"full_name": request.user.username })
	else:
		return HttpResponseRedirect('/login/login/')

def invalidlogin(request):
	return render_to_response('invalidlogin.html')


def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		u = UserType.objects.filter(user_name=username)
		if u[0].user_type=='manager':
			return render_to_response('loggedin.html', {'user': u})
		elif u[0].user_type=='employee':
			return render_to_response('loggedin.html',{'user':u})
		elif u[0].user_type=='customer':
			return render_to_response('loggedin.html', {'user': u})
		else:
			return render_to_response('errorpage.html', {'user': u})
	else:
		return HttpResponseRedirect('/login/invalidlogin/')


def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')
# Create your views here.
