import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Category
from ads.serializers import CategorySerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryListView(ListView):
#     queryset = Category.objects.order_by("name")
#     context_object_name = 'category_list'
#     paginate_by = settings.TOTAL_ON_PAGE
#
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         context = self.get_context_data()
#
#         response = {
#             "items": [
#                 category.json_representation for category in context['category_list']
#             ],
#             "total": context['paginator'].count if context['paginator'] is not None else len(context['category_list']),
#             "num_pages": context['paginator'].num_pages if context['paginator'] is not None else 1
#         }

        # return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryDetailView(DetailView):
#     queryset = Category.objects
#
#     def get(self, request, *args, **kwargs):
#         try:
#             category = self.get_object()
#         except Http404:
#             return JsonResponse({"Error": "Not found"}, status=404)

        # return JsonResponse(category.json_representation, json_dumps_params={'ensure_ascii': False})


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryCreateView(CreateView):
#     model = Category
#     fields = ["name"]
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         category = Category.objects.create(
#             name=data["name"]
#         )
#
#         return JsonResponse(category.json_representation, json_dumps_params={'ensure_ascii': False})


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryUpdateView(UpdateView):
#     model = Category
#     fields = ["name"]
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         category_data = json.loads(request.body)
#
#         self.object.name = category_data["name"]
#
#         self.object.save()
#
#         return JsonResponse({"name": self.object.name})


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryDeleteView(DeleteView):
#     model = Category
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)
