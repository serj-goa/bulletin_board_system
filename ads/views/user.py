import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import User, Location


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
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Http404:
            return JsonResponse({"Error": "Not found"}, status=404)

        return JsonResponse(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "address": user.location.address if user.location else None,
            },
            json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"]
        )

        for location in user_data["locations"]:
            location_object, created = Location.objects.get_or_create(address=location)
            user.locations.add(location_object)

        user.save()

        return JsonResponse(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all()))
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]

        for location in user_data["locations"]:
            location_object, created = Location.objects.get_or_create(name=location)
            self.object.locations.add(location_object)

        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "password": self.object.password,
                "role": self.object.role,
                "age": self.object.age,
                "locations": list(map(str, self.object.locations.all()))
            }
        )


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
