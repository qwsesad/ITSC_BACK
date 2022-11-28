from django.shortcuts import render

# Create your views here.
from .models import team_member
from .serializer import CustomizationSerializer
from rest_framework import generics

class CustomizationListGet(generics.ListCreateAPIView):
    queryset = team_member.objects.exclude(name='').exclude(name__isnull=True).exclude(
                                           spec='').exclude(spec__isnull=True).exclude(course__isnull=True)
    serializer_class = CustomizationSerializer

def home_page(request):
    data=team_member.objects.all()
    return render(request, 'home_page.html', {'data':data})