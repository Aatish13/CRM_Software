from django.shortcuts import render
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url = '/accounts/login/')
def dashboard(request):
	return render_to_response('empdashboard.html')