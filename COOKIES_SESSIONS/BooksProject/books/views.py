from django.http import HttpRequest
from django.shortcuts import render, redirect, resolve_url
from .forms import BookModelForm, CommentForm
from .models import Book, Comment


def index(request: HttpRequest):

    if 'favs_only' in request.GET:
        favs_books = request.session.get("favs", [])
        book_list = Book.objects.filter(id__in=favs_books)
    else:
        book_list = Book.objects.all()


    context = {"books": book_list, "display": True}

    response= render(request, 'index.html', context)


    if 'font_size' in request.GET:
        response.set_cookie('font_size', request.GET['font_size'])
    return response


def add_book(request: HttpRequest):
    if request.method == 'POST':
        bookModelForm = BookModelForm(request.POST, request.FILES)

        if bookModelForm.is_valid():
            book = bookModelForm.save()
            return redirect(resolve_url('books:index'))

    form = BookModelForm()
    return render(request, 'add_book.html', {"form": form})


def list_books(request: HttpRequest, book_index):

    if request.GET:
        print(request.GET)

    books = ["Titanic", "Monsters Inc.", "Toy Story"]
    print(book_index)
    context = {"book": books[int(book_index)]}
    return render(request, 'list.html', context)


def book_detail(request: HttpRequest, book_id):
    book = Book.objects.get(pk=book_id)

    # get the session data or none
    session_content = request.session.get("fav_books", None)
    print(session_content)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            added_comment = Comment(book=book, name=comment_form.cleaned_data["name"],
                                    content=comment_form.cleaned_data["content"])
            added_comment.save()
        else:
            print(comment_form.errors)

    context = {"book": book, "form": CommentForm()}

    return render(request, 'book_detail.html', context)


def add_favorite(request: HttpRequest, book_id):
    request.session["favs"] = request.session.get("favs", []) + [book_id]
    print(request.session["favs"])

    return redirect(resolve_url("books:index"))
