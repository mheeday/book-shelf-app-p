from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from .forms import CommentForm, UserRegistrationForm, BookForm
from .models import Books, UserBook, BookReview
from django.contrib.auth.forms import AuthenticationForm
import random
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import uuid
from django.conf import settings

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('user_home', username=request.user.username)
    
    context = {'context_home':{}}
    books = Books.objects.all()
    for cat_tuple in Books.BOOK_CATEGORIES:
        cat = cat_tuple[0]
        b_choice = random.choice(books.filter(book_cat=cat))
        print(cat, b_choice)
        context['context_home'][cat] = b_choice
    print(context)
    return render(request, 'mainlib/home.html', context)

@login_required
def user_home(request, username):
    if request.user.is_authenticated:
        userbooks = UserBook.objects.filter(user=request.user).order_by('-last_viewed')
        if userbooks.exists():
            context = {'item':{}}
            for cat_tuple in Books.BOOK_CATEGORIES:
                i = cat_tuple[0]
                cat_books = userbooks.filter(book__book_cat=i)
                if cat_books.exists():
                    context['item'][i] = list(cat_books)
            return render(request, 'mainlib/user_home.html', context)
        else:
            context = {'item': 0}
            return render(request, 'mainlib/user_home.html', context)

    else:
        messages.info(request, f"Please, Login.")
        return redirect('login')

def book_cat_list(request, category):
    category = category.capitalize()
    books = Books.objects.filter(book_cat=category)
    context = {'context_text':[], 'category':category}
    for book in books:
        context['context_text'].append(book)
    return render(request, 'mainlib/book_cat_list.html', context)

def update_date(user, book):
    try:
        temp_a = UserBook.objects.get(book=book, user=user)
        temp_a.last_viewed = timezone.now()
        temp_a.save()
        return True
    except:
        return False

@login_required
def per_book(request, book_id):
    
    book = get_object_or_404(Books, pk=book_id)

    context = {'book': book}

    try:
        temp_var = UserBook.objects.get(book=book)
        if temp_var.archived == True:
            context['buttons'] = {'sub':'Remove from Personal', 'unarc':'Unarchive Book', }

        else:
            context['buttons'] = {'sub':'Remove from Personal', 'arc':'Archive Book', }
    except:
        context['buttons'] = {'add':'Add to Personal'}

    new_review = None

    if request.method == 'POST' and 'comment' in request.POST:
        review_form = CommentForm(data=request.POST)
        if review_form.is_valid():
            new_review = BookReview(user=request.user, book=Books.objects.get(pk=book_id), rev=review_form.cleaned_data.get('rev'), date_posted = timezone.now())
            new_review.save()         
            return redirect('per_book', book_id)
    
    elif request.method == 'POST' and 'add' in request.POST:
        temp_var = UserBook(user=request.user, book=book, last_viewed=timezone.now())
        temp_var.save()

        temp_a = UserBook.objects.get(book=book)
        temp_a.last_viewed = timezone.now()
        temp_a.save()

        return redirect('per_book', book_id)

    elif request.method == 'POST' and 'sub' in request.POST:
        temp_var = UserBook.objects.get(book=book)
        temp_var.delete()
        return redirect('per_book', book_id)

    elif request.method == 'POST' and 'arc' in request.POST:
        temp_var = UserBook.objects.get(book=book)
        temp_var.archived = True
        temp_var.save()
        update_date(request.user, book)
        return redirect('per_book', book_id)

    elif request.method == 'POST' and 'unarc' in request.POST:
        temp_var = UserBook.objects.get(book=book)
        temp_var.archived = False
        temp_var.save()
        update_date(request.user, book)
        return redirect('per_book', book_id)

    else:
        review_form = CommentForm()
        context['form'] = review_form

    book_reviews = BookReview.objects.filter(book_id=book_id).order_by('-date_posted')

    if book_reviews.exists():
        context['reviews'] =  book_reviews
    return render(request, 'mainlib/each_book.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Welcome {form.cleaned_data['first_name']}!, account created successfully.")
            return redirect('login')

    else:
        form = UserRegistrationForm()

    context = {'form':form}
    return render(request, 'mainlib/register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Welcome back, {username}.")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
            else:
                messages.warning(request, "Invalid Username or Password!")
        else:
            messages.warning(request, "Invalid Username or Password!")
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'mainlib/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def all_user_books(request):
    books = UserBook.objects.filter(user=request.user, archived=False)
    if books.exists():
        context = {'books': []}
        for book in books:
            context['books'].append(book.book)
    else:
        context = {'empty': 'empty'}

    return render(request, "mainlib/all_user_books.html", context)

@login_required
def user_archive(request):
    books = UserBook.objects.filter(user=request.user, archived=True)
    if books.exists():
        context = {'books': []}
        for book in books:
            context['books'].append(book.book)
    else:
        context = {'empty': 'empty'}
    return render(request, "mainlib/user_archive.html", context)

@login_required
def add_book(request):
    if request.method == 'POST' and request.FILES['image_file']:
        print('YES ----', request.FILES['image_file'])
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book_title = form.cleaned_data.get('book_title')
            book_author = form.cleaned_data.get('book_author')
            book_cat = form.cleaned_data.get('book_cat')
            book_desc = form.cleaned_data.get('book_desc')
            book_pubd = form.cleaned_data.get('book_pubd')
            book_cover = uuid.uuid4()
            image = form.cleaned_data.get('image_file')

            temp_book = Books(book_title = book_title, book_author = book_author, book_cat = book_cat, book_cover = book_cover, book_desc = book_desc, book_pubd = book_pubd, book_image=image)
            temp_book.save()

            book = Books.objects.get(book_cover=book_cover)
            return redirect('per_book', book_id=book.id)

        else:
            messages.info(request, "Invalid Details, please check!")

    form = BookForm()
    context = {'form':form}
    return render(request, 'mainlib/add_book.html', context)