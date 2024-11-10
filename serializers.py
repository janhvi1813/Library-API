from rest_framework import serializers
from .models import Book, Borrower, Loan

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model"""
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'available', 'borrow_count']

class BorrowerSerializer(serializers.ModelSerializer):
    """Serializer for the Borrower model"""
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'membership_date', 'is_active']

class LoanSerializer(serializers.ModelSerializer):
    """Serializer for the Loan model"""
    book = BookSerializer(read_only=True)  # Nested serializer to show book details
    borrower = BorrowerSerializer(read_only=True)  # Nested serializer to show borrower details

    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrower', 'borrowed_date', 'return_date', 'is_returned']
