from django.shortcuts import render,redirect
from Inventory.models import Category, Product

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

        Product.objects.create(name=name, quantity=quantity, price=price, category_id=category)
        return redirect('add_item')  
    
    categories= Category.objects.all()
    items = Product.objects.all()
    return render(request, 'add_item.html', {'categories':categories, 'items':items})

def update_stock(request, item_id, action):
    product = Product.objects.get(id=item_id)
    if action == 'add':
        product.quantity += 1                               
    elif action == 'remove':
        product.quantity -= 1
    product.save()
    return redirect('add_item')    

def edit_item(request):
    items = Product.objects.all()
    return render(request, 'edit_item.html', {'items':items})
    
def update_product(request, item_id):
    product = Product.objects.get(id=item_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.quantity = request.POST['quantity']
        product.price = request.POST['price']
        product.category_id = request.POST['category']
        product.save()
        return redirect('edit_item')
        
    categories = Category.objects.all()
    return render(request, 'update_item.html', {'product': product, 'categories': categories})

def delete_item(request, item_id):
    product = Product.objects.get(id=item_id)
    product.delete()
    return redirect('edit_item')


