from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import CategoryForm
from rango.models import Category
from rango.models import Page
from rango.models import PageForm
from rango.models import UserForm
from rango.models import UserProfile
from rango.models import UserProfileForm

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('name')
    context_dict = {'categories': category_list}
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    return HttpResponse('This is the About page.')

def add_category(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
	if form.is_valid():
	    form.save(commit=True)
	    return index(request)
	else:
	    print form.errors
    else:
        form = CategoryForm()
    return render_to_response('rango/add_category.html', {'form': form}, context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
	profile_form = UserProfileForm(data=request.POST)
	if user_form.is_valid() and profile_form.is_valid():
	    user = user_form.save()
	    user.set_password(user.password)
	    user.save()
	    profile = profile_form.save(commit=False)
	    profile.user = user
	    profile.save()
	    registered = True
	else:
	    print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
	profile_form = UserProfileForm()
    return render_to_response(
    		'rango/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
	    if user.is_active:
	        login(request, user)
		return HttpResponseRedirect('/rango/')
	    else:
	        return HttpResponse('Your Rango account is disabled.')
	else:
	    return HttpResponse('Invalid username or password.')
    else:
        return render_to_response('rango/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
