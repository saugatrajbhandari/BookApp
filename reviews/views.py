from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.core.files.images import ImageFile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from io import BytesIO
from PIL import Image

from .models import Book, Review, Contributor, Publisher
from .utils import average_rating, check_permission
from .forms import (SearchForm, PublisherForm, ReviewForm, BookMediaForm,
                    LoginForm, ProfileForm, CustomUserCreationForm, BookForm, BookDetailForm)


def home(request):
    return redirect('book_list')


def book_search(request):
    search_text = request.GET.get('search', '')
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data['search']:
        search = form.cleaned_data['search']
        search_in = form.cleaned_data.get('search_in') or 'title'
        if search_in == 'title':
            books = Book.objects.filter(title__icontains=search)
        else:
            contributors = Contributor.objects.filter(Q(first_names__icontains=search)|Q(last_names__icontains=search))

            for contributor in contributors:
                for book in contributor.book_set.all():
                    books.add(book)

    return render(request, 'reviews/search-results.html', {'form': form, 'search_text': search_text, 'books': books})


def book_list(request):
    books = Book.objects.order_by('-id')
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    page_range = paginator.page_range
    book_obj = page_obj.object_list
    book_list = []
    for book in book_obj:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book, 'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})

    context = {'book_list': book_list, 'page_obj': page_obj, 'page_range': page_range}
    return render(request, 'reviews/books_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    form = ReviewForm(request.POST or None)
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.save()
        return redirect('book_detail', book.pk)
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {'book': book, 'book_rating': book_rating, 'reviews': reviews, 'form': form}
    else:
        context = {'book': book, 'book_rating': None, 'reviews': None, 'form': form}

    return render(request, 'reviews/book_detail.html', context)


@user_passes_test(check_permission)
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f"Publisher {updated_publisher} was created.")
            else:
                messages.success(request, f"Publisher {updated_publisher} was updated.")
            return redirect('publisher_edit',updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, 'reviews/publisher_edit.html', {'form': form, 'method': request.method})


@login_required(login_url='/accounts/login/')
def review_edit(request, book_pk, review_pk):
    review_obj = get_object_or_404(Review, pk=review_pk)
    if request.user != review_obj.creator:
        raise PermissionDenied
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review_obj)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = review_obj.book
            review.date_edited = timezone.now()
            review.creator = request.user
            form.save()
            messages.success(request, f'Review is updated successfully')
            return redirect('book_detail', review_obj.book.pk)
    else:
        form = ReviewForm(instance=review_obj)

    return render(request, 'reviews/review_edit.html', {'form': form})


def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            cover = form.cleaned_data.get('cover')
            if cover:
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data,format=cover.image.format)
                image_file=ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, "Book \"{}\" was successfully updated.".format(book))
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request, "reviews/book-media-form.html",
                  {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('book_list')
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('book_list')
        return super(CustomLogoutView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login')
def profile(request):
    state = None
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.instance.email == '' and form.instance.first_name == '' and form.instance.last_name == '':
            state = 'created'
        else:
            state = 'updated'
        if form.is_valid():
            form.save()
            messages.success(request, f'You profile successfully {state}')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'reviews/profile.html', {'form': form, 'state': state})


def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'reviews/signup.html', {'form': form})


def book_create(request, pk=None):
    if request.user.is_authenticated:
        if pk is not None:
            book_obj = get_object_or_404(Book, pk=pk)
            if book_obj.creator != request.user:
                raise PermissionDenied
        else:
            book_obj = None
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                book.creator = request.user
                book.save()
                return redirect('book_detail', book.id)
        else:
            form = BookForm()
        return render(request, 'reviews/bookcreate.html', {'form': form, 'book': book_obj})
    else:
        return redirect('login')


def book_update(request, pk):
    if request.user.is_authenticated:
        book_obj = get_object_or_404(Book, pk=pk)
        if book_obj.creator != request.user:
            raise PermissionDenied
        if request.method == 'POST':
            form = BookDetailForm(request.POST, request.FILES, instance=book_obj)
            if form.is_valid():
                book = form.save(commit=False)
                book.creator = request.user
                book.save()
                return redirect('book_detail', book.id)
        else:
            form = BookDetailForm(instance=book_obj)
        return render(request, 'reviews/bookupdate.html', {'form': form, 'book': book_obj})
    else:
        return redirect('login')