from scoreTest.test import *
#import mongotest
from django.shortcuts import render
from django.http import HttpResponse
import json
from scoreTest.models import *
from django.template import RequestContext
from pymongo import MongoClient


# def registrate(request):
# 	if request.POST:
# 		form = RegistrationForm(request.POST)
# 		if form.is_valid():
# 			#try:
# 				names = []
# 				data = json.loads(request.POST['jsonData'])
# 				for data in data:
# 					names.append(data['name'])

# 					user = User(name = data['name'], password = data['password'])
# 					user.save()

# 					for mail in data["emails"]:
# 						emails = Email(iduser = user, email = mail)
# 						emails.save()

# 				return HttpResponse("Users created: " + ', '.join(names) + "</br> Request: </br>" + request.POST['jsonData'])
# 			#except Exception as e:
# 				return HttpResponse("Error: " + str(e))
# 	else:
# 		form = RegistrationForm()
# 	return render( request, "registrate.html", {'form': form})


def index(request):
	# res = test.test_score()
    # return HttpResponse("Hello, world. You're at the polls index.")
    	# return render(request, "index.html", {'neg' : res.negative, 'pos': res.positive, 'neutral': res.neutral})
	# if request.method=='GET':
	# 	client = MongoClient('mongodb://192.168.1.7:27017/')
	# 	featureCountCollection = db['FeatureCount']
	# 	res = featureCountCollection.find_one({'name': 'iphone6', 'feature':'camera'})
	# 	return render(request, "index.html", res['pos'])
	# else:
		return render(request, "index.html", {})


def test(request):
	print "IN"
	if request.method=='GET':
		print "Chart"
		resp=test_score()
		result=[]
		result1={'neg' : resp.negative, 'pos': resp.positive, 'neutral': resp.neutral}
		result.append(result1)
		
    	return HttpResponse(json.dumps(result),  content_type="application/json")

def render_sentiment(request):
	print "Abinaya"
	if request.method=='GET':
		product=request.GET.get('product')
		feature=request.GET.get('feature')
		client = MongoClient('mongodb://neha:mongo@ds031632.mongolab.com:31632/sentiment')
		db = client.get_default_database()
		featureCountCollection = db['FeatureCount']
		res = featureCountCollection.find_one({'name': product.lower(), 'feature':feature.lower()})
		return HttpResponse(json.dumps(res['pos']),  content_type="application/json")

def cloud_render(request):

	if request.method=='GET':
		product=request.GET.get('product')
		feature=request.GET.get('feature')
		client = MongoClient('mongodb://neha:mongo@ds031632.mongolab.com:31632/sentiment')
		db = client.get_default_database()
		featureCountCollection = db['FeatureCount']
		res = featureCountCollection.find_one({'name': product.lower(), 'feature':feature.lower()})		
		print json.dumps(res['neg'])
		return HttpResponse(json.dumps(res['neg']),  content_type="application/json")

def feature_sentiment(request):
	print "Abinaya"
	if request.method=='GET':
		product=request.GET.get('product')
		feature=request.GET.get('feature')
		client = MongoClient('mongodb://neha:mongo@ds031632.mongolab.com:31632/sentiment')
		db = client.get_default_database()
		featureCountCollection = db['FeatureCount']
		res = featureCountCollection.find_one({'name': product.lower(), 'feature':feature.lower()})
		print res['pos']
		return HttpResponse(json.dumps(res['pos']),  content_type="application/json")

def overall_sentiment(request):
	if request.method=='GET':
		product=request.GET.get('product')
		client = MongoClient('mongodb://neha:mongo@ds031632.mongolab.com:31632/sentiment')
		db = client.get_default_database()
		sentCollection = db['OverallSentiment']
		res=sentCollection.find_one({'name': product.lower()});
		data={}
		data["pos"]=json.dumps(res['pos'])
		data["neg"]=json.dumps(res['neg'])
		data["neutral"]=json.dumps(res['neutral'])
		print data
		return HttpResponse(json.dumps(data),  content_type="application/json")


		





# Create your views here.
