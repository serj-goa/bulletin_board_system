from rest_framework import serializers as s

from ads.models import Ad, User


class AdSerializer(s.ModelSerializer):
    author = s.SlugRelatedField(read_only=True, slug_field='username')
    category = s.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateUpdateSerializer(s.ModelSerializer):
    # author = s.PrimaryKeyRelatedField(queryset=User.objects.filter(role='member'))
    # author = s.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Ad
        # fields = '__all__'
        exclude = ['author']
