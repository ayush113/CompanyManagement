from django.db import models
from django.contrib.auth.models import User
from custsupport.models import Customer

# Create your models here.

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=40, blank=True, null=True)
    leader = models.ForeignKey(User, models.DO_NOTHING, db_column='leader', blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'project'
