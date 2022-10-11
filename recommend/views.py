from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from django.template import loader
from recommend.models import Recommend
from django.http.response import HttpResponse

# Create your views here.
class BestprodView(View):
    def get(self, request ) :
        pass
    def post(self):
        pass