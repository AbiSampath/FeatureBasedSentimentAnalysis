import pymongo
import yaml
import re
import csv
import random
from pymongo import MongoClient
from bson.json_util import dumps
import json


def merge_data(x, y):

    return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}


productSet = set([])
featureSet = set([])
positiveSet = set([])
negativeSet = set([])


client = MongoClient('mongodb://localhost:27017/')

db = client['Sentiment']
productCollection = db['Product']
featureCountCollection = db['FeatureCount']

# Get all products from DB
for row in productCollection.find():
    productName = row.get("product_name")
    productSet.add(productName)

featureCollection = db['Features']

# Get all features from DB
for row in featureCollection.find():
    featureName = row.get("feature_name")
    featureSet.add(featureName)

# Load positive words into a set
positiveStream = open("positive.yml", "r")
positiveDocs = yaml.load_all(positiveStream)

for row in positiveDocs:
    for k, v in row.items():
        positiveSet.add(k)

# Load negative words into a set
negativeStream = open("negative.yml", "r")
negativeDocs = yaml.load_all(negativeStream)

for row in negativeDocs:
    for k, v in row.items():
        negativeSet.add(k)

def subText(s, t):
	for sub in s:

		if sub in t:
			print sub
			return sub

with open("reviews.csv", "rU") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        text = ''.join(row)
        text = text.lower()
        pos = positiveSet.intersection(text.split())
        neg = negativeSet.intersection(text.split())
        feature = subText(featureSet, text)
        product = subText(productSet, text)
        data = {}
        dataPos = {}
        dataNeg = {}

        if product and feature:
            if pos:
                for posId in set(pos):
                    dataPos[posId] = 1
            data['pos'] = dataPos
            if neg:
                for negId in set(neg):
                    dataNeg[negId] = 1
            data['neg'] = dataNeg

            data['name'] = product
            data['feature'] = feature
        if data:
        	res = featureCountCollection.find_one({'name': product, 'feature':feature})
        	if res:
        		if dataPos:
	        		featureCountCollection.update({'_id':res['_id']},{'$set':{'pos': merge_data(res['pos'],data['pos'])}}, upsert=False, multi=False)
	        	if dataNeg:
	        		featureCountCollection.update({'_id':res['_id']},{'$set':{'neg': merge_data(res['neg'],data['neg'])}}, upsert=False, multi=False)
        	else:
        		featureCountCollection.insert(data)

        # if res:
        # 	x = res['pos']
        # 	resPos = merge_data(x,dataPos)
        # 	print resPos
        # data['pos'] =resPos
        # featureCountCollection.find_one_and_replace({'name': prd},data)
        # else:
        # 	resPos = dataPos
        # 	featureCountCollection.insert(data)

        # featureCountCollection.insert(data)