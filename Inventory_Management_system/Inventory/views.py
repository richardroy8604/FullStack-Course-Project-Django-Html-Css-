from django.shortcuts import render

# Create your views here.
 
def home(request):
    return render(request, 'home.html')

def add_item(request):
    if request.method == 'POST':
        # Process the form data
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        category = request.POST['category']
        # Save the data to the database or perform other actions
    return render(request, 'add_item.html')


