from django.db import models

class Recommend(models.Model):
	username = models.CharField(max_length=255)
	age = models.IntegerField(max_length=5)
	product = models.CharField(max_length=255)
	feature = models.CharField(max_length=255)