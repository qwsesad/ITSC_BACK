from django.shortcuts import render

# Create your views here.
from .models import team_member


def home_page(request):
    data=team_member.objects.all()
    return render(request, 'home_page.html', {'data':data})