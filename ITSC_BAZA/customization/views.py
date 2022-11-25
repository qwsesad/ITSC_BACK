from django.shortcuts import render

# Create your views here.
from .models import team_member
from .serializer import CustomizationSerializer
from rest_framework import generics

class CustomizationListGet(generics.ListCreateAPIView):
    queryset = team_member.objects.all()
    serializer_class = CustomizationSerializer

def home_page(request):
    data=team_member.objects.all()
    return render(request, 'home_page.html', {'data':data})