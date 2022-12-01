import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Location, User


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    queryset = User.objects.select_related("location").order_by("role", "username")
    context_object_name = 'users_list'
    paginate_by = settings.TOTAL_ON_PAGE

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        response = {
            "items": [
                user.json_representation for user in context['users_list']
            ],
            "total": context['paginator'].count if context['paginator'] is not None else len(context['users_list']),
            "num_pages": context['paginator'].num_pages if context['paginator'] is not None else 1,
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(DetailView):
    queryset = User.objects.select_related("location")

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Http404:
            return JsonResponse({"Error": "Not found"}, status=404)

        return JsonResponse(user.json_representation, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        location_data = data['location']
        location = Location.objects.create(
            address=location_data['address'],
            latitude=location_data['latitude'],
            longitude=location_data['longitude'],
        )

        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=data["password"],
            role=data["role"],
            age=data["age"],
            location=location,
        )

        return JsonResponse(user.json_representation, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    queryset = User.objects.filter(is_active=True)

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = self.get_object()

        if 'first_name' in data:
            user.first_name = data["first_name"]
        if 'last_name' in data:
            user.last_name = data["last_name"]
        if 'username' in data:
            user.username = data["username"]
        if 'password' in data:
            user.set_password(data["password"])
        if 'role' in data:
            user.role = data["role"]
        if 'age' in data:
            user.age = data["age"]
        if 'location' in data:
            if user.location is None:
                location = Location.objects.create(
                    address=data['location']['address'],
                    latitude=data['location']['latitude'],
                    longitude=data['location']['longitude'],
                )
                user.location = location
            else:
                location = user.location
                if 'address' in data['location']:
                    location.address = data['location']['address']
                if 'latitude' in data['location']:
                    location.latitude = data['location']['latitude']
                if 'longitude' in data['location']:
                    location.longitude = data['location']['longitude']
                location.save()
        user.save()

        return JsonResponse(user.json_representation, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserAdDetailView(View):
    def get(self, request):
        user_qs = User.objects.prefetch_related("locations")\
                      .annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        users = []

        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    # "location": list(map(str, user.locations.all())),
                    "total_ads": user.total_ads
                }
            )

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False)
