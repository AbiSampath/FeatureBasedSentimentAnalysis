from django.shortcuts import render_to_response, render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from forms import ProductFeatureForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from mysite.models import Recommend
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from operator import itemgetter
import simplejson
import itertools
age = 0
name = ""
res_final = ""

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)

def home(request):
	c={}
	c.update(csrf(request))
	return render_to_response('home.html', c)

def login(request):
	c={}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')

def loggedin2(request):
	cursor = connection.cursor()
	cursor.execute("SELECT user_age FROM auth_user WHERE username=%s", [request.user.username])
	
	dataArr=[]
	urlArr=[]
	prodArr=[]
	feaArr=[]


	dictJSON={'Iphone6':'/static/img/iphone6.jpg','Samsung Galaxy S6':'/static/img/S6.jpg',
	'OnePlus One':'/static/img/one.jpg','Samsung Galaxy Note':'/static/img/galaxynote.jpg',
	'HTC Desire One':'/static/img/htc.jpg'}
	global age
	global name
	global res_final
	age = cursor.fetchone()
	name = request.user.username
	#cursor.execute("SELECT product,feature FROM mysite_recommend WHERE age=%s ",[age] )
	cursor.execute("SELECT product,feature,COUNT(feature) from mysite_recommend WHERE age=%s GROUP BY product,feature",[age])
	for row in cursor:
		data={}
		data['product']=row[0]
		data['feature']=row[1]
		data['count']=row[2]
		dataArr.append(data)
		
	# row = cursor.fetchone()
	# print json.dumps(row)
	#print ("People of your age also looked for: ",row)
	str=json.loads(json.dumps(dataArr))
	#print str

	jsonObj=sorted(str,key=itemgetter('count'),reverse=True)
	newJSON=itertools.islice(jsonObj, 6)
	print newJSON
	for obj in newJSON:
		print obj['product'],obj['feature']
		prodArr.append((obj['product'])+" "+ obj['feature'])
		urlArr.append(dictJSON.get(obj['product']))

	print urlArr
	


	return render_to_response('loggedin2.html',{'full_name' : request.user.username,'rows' : json.dumps(jsonObj),'urls':simplejson.dumps(urlArr),'prodFeature':simplejson.dumps(prodArr)})

	#return HttpResponse(json.dumps(row),content_type = "application/json")

def invalid_login(request):
	return render_to_response('invalid_login.html')



def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')
		else:
			return render_to_response('registration_failed.html')

	args = {}
	args.update(csrf(request))
	args['form'] = MyRegistrationForm()
	print args
	return render_to_response('register.html', args)

def register_success(request):
	return render_to_response('register_success.html')

@csrf_exempt
def product(request):
		selected_option1 = request.POST.get("product_selection","")
		selected_option2 = request.POST.get("feature_selection","")
		print("product is: ",selected_option1," feature is: ", selected_option2)
		response_data = {}
		if selected_option1!="":
			print selected_option1
			if selected_option2!="":
				print selected_option2
				try:
					cursor = connection.cursor()
					cursor.execute("INSERT into mysite_recommend (username, age, product,feature) VALUES (%s, %s, %s, %s)", [name,age,selected_option1,selected_option2])
					response_data['message1'] = selected_option1
					response_data['message2'] = selected_option2
	
				except:
					response_data['message'] = "error"

		return HttpResponse(json.dumps(response_data),content_type = "application/json")


def about(request):
	return render_to_response('about.html')

def architecture(request):
	return render_to_response('architecture.html')

def index(request):
	return render_to_response('index.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def log_me_out(request):
	logout(request)
	return HttpResponseRedirect('/accounts/login')



