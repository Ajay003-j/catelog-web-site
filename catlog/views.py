from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User  # FIXED: Added missing import
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login as auth_login # FIXED: Aliased to avoid function name clash
from django.contrib.auth.mixins import LoginRequiredMixin # FIXED: Used Mixin for CBVs instead of decorator
from django.views import generic
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

from .models import Book, Notes
from .forms import BookForm, SiginForm, NoteForm

def index(request):
    return HttpResponse("Welcome to the library")

def about(request):
    return HttpResponse("This is the library")

@login_required
def note_list(request):
    notes = Notes.objects.filter(owner = request.user)
    return render(request, 'catlog/notes_list.html', {'notes',notes})

@login_required
def note_details(request):
    notes = get_object_or_404(Notes, id=pk, owner=request.user)
    return render(request, 'catlog/notes_details.html', {'notes':notes})

@permission_required('catlog.add_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note-details')
    else:
        form = NoteForm()
    return render(request, '', {'form':form})

def book_list(request, pk):
    books = NoteForm.objects.filter()

# FIXED: Inherit from LoginRequiredMixin instead of applying decorator
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 1
    ordering = ['title']

# FIXED: Inherit from LoginRequiredMixin instead of applying decorator
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

def send_verification_email(request, user):
    """Generates a fresh token and dispatches the email."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(reverse('activate', args=[uid, token]))
    
    send_mail(
        "Verify your account",
        f"Hi {user.username}, click to activate your account:\n{link}",
        None,
        [user.email] 
    )


def register(request):
    if request.method == 'POST':
        form = SiginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_verification_email(request, user)

            return render(request, 'registration/resend_verfication.html', {'unverified_user': user})
    else:
        form = SiginForm()
    return render(request, 'registration/register.html', {'form': form})

def resend_activation(request, user_id):
    """Fetches an inactive user and sends a fresh activation link."""
    user = get_object_or_404(User, pk=user_id, is_active=False)
    
    # Fire off a brand new email with a fresh timestamp token
    send_verification_email(request, user)
    
    # Return them back to the same confirmation page with a success flag
    return render(request, 'registration/resend_verfication.html', {
        'unverified_user': user,
        'resent': True
    })

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None   

    if user is not None and default_token_generator.check_token(user, token): 
        user.is_active = True
        user.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')
    return render(request, 'registration/activation_invalid.html')

def login_view(request): 
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error = "Wrong username or password"
            
    return render(request, 'registration/login.html', {'error': error})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            return redirect('book-detail', pk=new_book.pk)
    else:
        form = BookForm()
    return render(request, 'catlog/add_book.html', {'form': form})
