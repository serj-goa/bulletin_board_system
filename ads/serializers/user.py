from rest_framework import serializers as s

from ads.models import Location, User


class UserSerializer(s.ModelSerializer):
    locations = s.SlugRelatedField(read_only=True, many=True, slug_field='name')

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(s.ModelSerializer):
    locations = s.SlugRelatedField(many=True, queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.initial_data = self.initial_data.copy()
        self._locations = self.initial_data.pop('address', [])

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)

        for location in self._locations:
            location_object, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_object)

        user.save()
        return user


class UserUpdateSerializer(s.ModelSerializer):
    locations = s.SlugRelatedField(required=False, many=True, slug_field='name', queryset=Location.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.initial_data = self.initial_data.copy()
        self._locations = self.initial_data.pop('address', [])

        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save()

        for location in self._locations:
            location_object, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_object)

        user.save()
        return user


# class UserAdSerializer(s.ModelSerializer):
#     total_ads = s.IntegerField()
#     location = s.SlugRelatedField(slug_field='location', many=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = "__all__"
