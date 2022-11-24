from django.db import models

class team_member(models.Model):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    DEFAULT = 'default'
    COLOR_CHOICES = [
        (RED, 'RED'),
        (BLUE, 'BLUE'),
        (GREEN, 'GREEN'),
        (DEFAULT, 'DEFAULT'),
    ]
    tg_id = models.IntegerField(unique=True, null=False, blank=False)
    tg_name = models.CharField(max_length=100, null=False, blank=False, default="aboba")
    secret_role = models.IntegerField(default=1)
    name = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='default')
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    role = models.CharField(max_length=100, null=True, blank=True)
    spec = models.CharField(max_length=200, null=True, blank=True)
    course = models.IntegerField(null=True, blank=True)
    inf_about = models.TextField(null=True, blank=True)
