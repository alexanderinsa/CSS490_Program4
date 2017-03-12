from __future__ import unicode_literals

from django.db import models

class Query(models.Model):
		url = models.CharField(max_length=100)
		pull_time = models.DateTimeField('date queried')
		text = models.CharField(max_length=5000000)

		def __str__(self):
			return self.url


# Create your models here.
