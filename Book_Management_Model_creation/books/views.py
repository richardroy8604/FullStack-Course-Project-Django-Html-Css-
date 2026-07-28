import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book

def index(request):
    edit_id = request.GET.get("edit_id")
    edit_book = None
    if edit_id:
        edit_book = Book.objects.filter(id=edit_id).first()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            name = request.POST.get("name")
            author = request.POST.get("author")
            year_of_publication = request.POST.get("year_of_publication")
            price = request.POST.get("price")
            number_of_pages = request.POST.get("number_of_pages")

            if name and author and year_of_publication and price and number_of_pages:
                Book.objects.create(
                    name=name,
                    author=author,
                    year_of_publication=int(year_of_publication),
                    price=float(price),
                    number_of_pages=int(number_of_pages)
                )
                messages.success(request, "Book added successfully!")

        elif action == "update":
            book_id = request.POST.get("book_id")
            book = Book.objects.filter(id=book_id).first()
            if book:
                book.name = request.POST.get("name", book.name)
                book.author = request.POST.get("author", book.author)
                book.year_of_publication = int(request.POST.get("year_of_publication", book.year_of_publication))
                book.price = float(request.POST.get("price", book.price))
                book.number_of_pages = int(request.POST.get("number_of_pages", book.number_of_pages))
                book.save()
                messages.success(request, f"Book with ID {book_id} updated successfully!")
            else:
                messages.error(request, f"Book with ID {book_id} does not exist!")

        elif action == "delete":
            book_id = request.POST.get("book_id")
            if book_id:
                deleted_count, _ = Book.objects.filter(id=book_id).delete()
                if deleted_count > 0:
                    messages.success(request, f"Book with ID {book_id} deleted successfully!")
                else:
                    messages.error(request, f"Book with ID {book_id} does not exist!")

        return redirect("/")

    books = Book.objects.all().order_by("id")

    # Serialize books list to JSON for instant client-side autofill on typing ID
    books_data = [
        {
            "id": b.id,
            "name": b.name,
            "author": b.author,
            "year_of_publication": b.year_of_publication,
            "price": str(b.price),
            "number_of_pages": b.number_of_pages
        }
        for b in books
    ]
    books_json = json.dumps(books_data)

    context = {
        "books": books,
        "books_json": books_json,
        "edit_book": edit_book,
    }
    return render(request, "index.html", context)
