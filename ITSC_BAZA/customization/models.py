from django.db import models

class team_member(models.Model):
    tg_id = models.IntegerField(unique=True, null=False, blank=False)
    tg_name = models.CharField(max_length=100, null=False, blank=False, default="aboba")
    secret_role = models.IntegerField(default=1)
    name = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    spec = models.CharField(max_length=200, null=True, blank=True)
    course = models.IntegerField(null=True, blank=True)
    inf_about = models.TextField(null=True, blank=True)
