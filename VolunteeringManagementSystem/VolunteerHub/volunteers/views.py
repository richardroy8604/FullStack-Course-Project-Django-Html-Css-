from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def accounts(request):
    return render(request,'index.html')
def volunteers(request):
    return render(request,'volunteers.html')
def events(request):
    return render(request,'events.html')
