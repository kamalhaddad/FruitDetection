from rest_framework import serializers
from .models import ClassificationImage

class ClassificationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationImage
        fields = '__all__'