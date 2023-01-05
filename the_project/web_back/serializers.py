from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('user_id','user_pass','user_name','user_admin','login_state')