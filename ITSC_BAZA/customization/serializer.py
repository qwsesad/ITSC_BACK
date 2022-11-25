from rest_framework import serializers
from .models import team_member

class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = team_member
        fields = ('tg_id', 'tg_name', 'secret_role', 'name', 'color', 'photo', 'role', 'spec', 'course', 'inf_about')