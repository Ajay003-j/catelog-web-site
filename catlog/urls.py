from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('books/', views.BookListView.as_view(), name='book-list'), # FIXED: Appended .as_view()
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'), # FIXED: Appended .as_view()
    path('accounts/sigin/', views.register, name='sigin'),
    path('books/add_book/', views.add_book, name='add-book'),
    path('accounts/login/', views.login_view, name='login'), # FIXED: Pointed to renamed login view function
    path('accounts/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('accounts/resend-verification/<int:user_id>/', views.resend_activation, name='resend-verification'), # FIXED: Added parameterized routing
]
