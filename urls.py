from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # List all books
    path('books/add/', views.add_book, name='add_book'),  # Add a new book
    path('borrow/', views.borrow_book, name='borrow_book'),  # Borrow a book
    path('api/borrowers/add/', views.add_borrower, name='add_borrower'),
    path('borrower/<int:borrower_id>/', views.get_borrower, name='get_borrower'),
    path('borrowed/<int:borrower_id>/', views.borrowed_books, name='borrowed_books'),  # List active (unreturned) books for a borrower
    path('history/<int:borrower_id>/', views.borrow_history, name='borrow_history'),  # List all books ever borrowed by a borrower, including return status
    path('return/', views.return_book, name='return_book'),  # Return a borrowed book
]
