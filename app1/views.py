from django.shortcuts import render
from django.http import HttpResponse
from .models import Division,Page
# Create your views here.
def index(request):
     page_list = Page.objects.order_by('-views')[:5]
     return render(request,'app1/index.html',{'page_list':page_list})
