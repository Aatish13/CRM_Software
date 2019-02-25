from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from loginModule.forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render_to_response
from loginModule.models import UserType
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
			form.save()
			u = UserType(user_type=user_type)
			u.save
			return render(request,'home.html')
	else:
		form = SignUpForm()
	args = {'form': form}
	return render(request, 'signup.html', args)


# Create your views here.
