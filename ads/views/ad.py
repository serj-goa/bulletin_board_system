import json

from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, User
from ads.serializers import AdSerializer, AdCreateUpdateSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def filter_queryset(self, queryset):
        request = self.request
        cat = request.GET.get('cat')
        text = request.GET.get('text')
        location = request.GET.get('location')
        price_from = request.GET.get('price_from', 0)
        price_to = request.GET.get('price_to', 1000000000)

        if cat:
            queryset = queryset.filter(category__id__exact=cat)

        if text:
            # self.queryset = self.queryset.filter(name__icontains=text)
            queryset = queryset.filter(name__icontains=text.lower())

        if location:
            # self.queryset = self.queryset.filter(author__locations__name__icontains=location)
            queryset = queryset.filter(author__location__address__icontains=location)

        if price_from or price_to:
            queryset = queryset.filter(price__range=[price_from, price_to])

        return super().filter_queryset(queryset)



# @method_decorator(csrf_exempt, name="dispatch")
# class AdListView(ListView):
#     queryset = Ad.objects.select_related("author", "category").order_by("-price")
#     context_object_name = 'ads_list'
#     paginate_by = settings.TOTAL_ON_PAGE
#
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         context = self.get_context_data()
#         response = {
#             "items": [
#                 ad.json_representation for ad in context['ads_list']
#             ],
#             "total": context['paginator'].count if context['paginator'] is not None else len(context['ads_list']),
#             "num_pages": context['paginator'].num_pages if context['paginator'] is not None else 1
#         }
#         return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class AdDetailView(DetailView):
#     queryset = Ad.objects.select_related("author", "category")
#
#     def get(self, request, *args, **kwargs):
#         try:
#             ad = self.get_object()
#         except Http404:
#             return JsonResponse({"Error": "Not found"}, status=404)
#
#         return JsonResponse(ad.json_representation, json_dumps_params={'ensure_ascii': False})

class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# @method_decorator(csrf_exempt, name="dispatch")
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "is_published", "category"]
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         try:
#             author = User.objects.get(pk=data['author'])
#             category = Category.objects.get(pk=data['category'])
#         except User.DoesNotExist:
#             return JsonResponse({"Error": "Author not exist."}, status=404)
#         except Category.DoesNotExist:
#             return JsonResponse({"Error": "Category not exist."}, status=404)
#
#         ad = Ad.objects.create(
#             name=data["name"],
#             author=author,
#             price=data["price"],
#             description=data["description"],
#             is_published=data["is_published"],
#             category=category,
#         )

        # return JsonResponse(ad.json_representation, json_dumps_params={'ensure_ascii': False})


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateUpdateSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "is_published", "category"]
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         ad_data = json.loads(request.body)
#
#         self.object.name = ad_data["name"]
#         self.object.author_id = ad_data["author"]
#         self.object.price = ad_data["price"]
#         self.object.description = ad_data["description"]
#         self.object.is_published = ad_data["is_published"]
#         self.object.category_id = ad_data["category"]
#
#         self.object.save()
#
#         return JsonResponse(
#             {
#                 "id": self.object.id,
#                 "name": self.object.name,
#                 "author": self.object.author_id,
#                 "price": self.object.price,
#                 "description": self.object.description,
#                 "is_published": self.object.is_published,
#                 "category": self.object.category_id
#             }
#         )
#


class AdImageView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class AdImageView(UpdateView):
#     model = Ad
#     fields = ["name", "image"]
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         self.object.image = request.FILES["image"]
#
#         self.object.save()
#
#         return JsonResponse(
#             {
#                 'id': self.object.id,
#                 'name': self.object.name,
#                 'image': self.object.image.url if self.object.image else None
#             }
#         )


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)


