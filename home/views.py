from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.core.cache import cache
from django.http import JsonResponse,FileResponse,HttpResponse
from PyPDF2 import PdfReader
from django.contrib import messages
from django.contrib.auth.models import User
import os, fitz
from io import BytesIO
from PIL import Image
from NovelNest.settings import MEDIA_URL
from django.contrib.auth import  login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required
def home(request):
    # print(request.user.id)
    colors = [c for c in range(200, 900, 100)]
    books = Book.objects.all().order_by('-added_date')[:6] 
    genres = Genre.objects.all()[:6]
    
    books_with_colors = [{'color': colors[i % len(colors)], 'book': book} for i, book in enumerate(books)]
    genres_with_colors = [{'color': colors[i % len(colors)], 'genre': genre} for i, genre in enumerate(genres)]
    
    return render(request, 'index.html', {
        'books_with_colors': books_with_colors,
        'genres_with_colors': genres_with_colors,
    })

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        login_id = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=login_id, password=password)
        
        if user is None:
            try:
                profile = UserProfile.objects.get(phone_number=login_id)
                user = authenticate(request, username=profile.user.username, password=password)
            except Exception as error:
                user = None
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Invalid credentials.'
            })
                
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     user=form.get_user()
        #     login(request,user)
        #     return redirect('home')
        # else:
        #     return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    return render(request, 'login.html', {'form': AuthenticationForm()})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def update_user(request):
    
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST,instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            
            messages.success(request,"Your Profile has been updated")
            return redirect('update_user')
        else :
            messages.error(request, "Error in Updating Profile")
            return redirect('update_user')
    else :
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html',{
        "user" : request.user,
        "user_form" : user_form,
        "profile_form" : profile_form
    })

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data["phone_number"]
            profile_picture = form.cleaned_data.get("profile_picture")
            UserProfile.objects.create(
                user=user,
                phone_number = phone_number,
                profile_picture = profile_picture
            )
            
        # username = request.POST.get('username')
        # firstname = request.POST.get('firstname')
        # lastname = request.POST.get('lastname')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        
        # user_existing = User.objects.filter(username=username).first()
        # if user_existing :
        #     return JsonResponse({"error":"User already exists"}, status=500) 
        
        # user = User.objects.create_user(username,email,password)
        # user.first_name = firstname
        # user.last_name = lastname
        # user.save()
        
            return redirect('login')
    else:
        form = UserRegisterForm()
            
    return render(request, 'register.html',{"form" : form})

@login_required
def get_books(request):
    books = Book.objects.all()
    return render(request,'books_admin.html',{'books':books})

def get_specific_book(request,book_id):
    
    book = Book.objects.filter(id=book_id).first()
    suggestions = Book.objects.exclude(id=book_id)
        
    return render(request,'book.html',{"book":book,'suggestions':suggestions})

@login_required
def download_pdf(request,book_id):
    book = Book.objects.filter(id=book_id).first()
    file_path = book.pdf_file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path,'rb'), as_attachment=True, filename=f"{book.name}.pdf")

@login_required
def get_genres(request):
    genres = Genre.objects.all()
    return render(request,'genre.html',{'genres':genres})

def get_book_page(request, book_id=None, page_number=None):
    
    cache_key = f"book_{book_id}_page_{page_number}"
    cached_img = cache.get(cache_key)
    if cached_img:
        return HttpResponse(cached_img, content_type='image/png')
    
    try:
        book = get_object_or_404(Book, id=book_id)
        pdf_path = book.pdf_file.path
        
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        cache.set(cache_key, img_byte_arr.getvalue(), timeout=300)

        return HttpResponse(img_byte_arr, content_type='image/png')
        
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)

def get_book_content(request, book_id):
    
    book = get_object_or_404(Book,id=book_id)
    
    with open(book.pdf_file.path,'rb') as f:
        reader = PdfReader(f)
        return render(request,'read_book.html', {
            "page_length" : len(reader.pages),
            "book" : book
        })

def collection(request):
    
    if request.method == "POST" :
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book,id=book_id)
        collection = Collection.objects.create(
            user = request.user,
            book = book
        )
        collection.save()
        return JsonResponse()
    else:
        return render(request, 'collection.html')

    

def user_profile(request,username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile,user=user)
    readlist = get_object_or_404(ReadList,user=user)
    
    return render(request, 'user_profile.html' , {'profile':profile, 'readlist' : readlist})

def book_suggestions(request):
    user = request.user
    favourite_genres = UserProfile.objects.filter(user=user).values_list('favourite_genres__name')
    collection = Collection.objects.filter(user=user).values_list('book', flat=True)

    return render(request, 'index.html',{'favourite_genres':favourite_genres,'collection':collection})

