from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'), 
    path('accounts/sigin/', views.register, name='sigin'),
    path('books/add_book/', views.add_book, name='add-book'),
    path('accounts/login/', views.login_view, name='login'), 
    path('accounts/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('accounts/resend-verification/<int:user_id>/', views.resend_activation, name='resend-verification'), 
    path('notes/', views.note_list, name='notes-list'),
    path('notes/<int:pk>/', views.note_details, name='notes-details'),
    path('notes/create_notes/', views.note_create, name='create-notes'),
]
