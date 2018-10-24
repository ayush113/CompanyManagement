from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    complaints = models.TextField(blank=True, null=True)
    bills = models.TextField(blank=True, null=True)
    changes = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    point_of_contact = models.ForeignKey(User, models.DO_NOTHING, db_column='point_of_contact', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'