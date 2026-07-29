from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact

# Create your views here.
def accounts(request):
    return render(request, 'index.html')

def add_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact_number = request.POST.get("contact_number")

        Contact.objects.create(
            name=name,
            contact_number=contact_number
        )
        return redirect("add_contact")

    cont = Contact.objects.all()
    return render(request, "contact.html", {"cont": cont})

