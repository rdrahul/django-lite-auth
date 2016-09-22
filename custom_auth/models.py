from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OAuthUser(models.Model):
    id = models.CharField( max_length=50 )
    first_name = models.CharField( max_length = 50)
    last_name = models.CharField( max_length = 50)
    email_address = models.CharField(max_length = 100 )
    access_token = models.CharField(max_length = 255)
    expiration_date = models.DateTimeField(null=True)
