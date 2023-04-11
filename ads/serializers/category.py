from rest_framework import serializers as s

from ads.models import Category


class CategorySerializer(s.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
