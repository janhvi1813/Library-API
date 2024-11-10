from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, Borrower, Loan
from .serializers import BookSerializer, LoanSerializer

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Library API. Go to /api/ for available endpoints.")



@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_books(request):
    available = request.GET.get('available')
    books = Book.objects.all()
    if available:
        books = books.filter(available=available.lower() == 'true')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_borrower(request):
    serializer = BorrowerSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_borrower(request, borrower_id):
    try:
        borrower = Borrower.objects.get(id=borrower_id)
    except Borrower.DoesNotExist:
        return Response({"detail": "Borrower not found."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(BorrowerSerializer(borrower).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def borrow_book(request):
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    book = get_object_or_404(Book, id=book_id)
    borrower = get_object_or_404(Borrower, id=borrower_id)

    if not borrower.is_active:
        return Response({"error": "Borrower membership is inactive."}, status=status.HTTP_403_FORBIDDEN)

    active_loans = Loan.objects.filter(borrower=borrower, is_returned=False).count()
    if active_loans >= 3:
        return Response({"error": "Borrower has reached the borrowing limit of 3 books."}, status=status.HTTP_403_FORBIDDEN)

    if not book.available:
        return Response({"error": "Book is currently unavailable."}, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.create(book=book, borrower=borrower)
    book.available = False
    book.borrow_count += 1
    book.save()

    return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def return_book(request):
    book_id = request.data.get('book_id')
    borrower = get_object_or_404(Borrower, id=borrower_id)
    book = get_object_or_404(Book, id=book_id)
    loan = Loan.objects.filter(book=book, borrower=borrower, is_returned=False).first()

    if loan:
        loan.is_returned = True
        loan.return_date = timezone.now()
        loan.save()

        book.available = True
        book.save()

        return Response(LoanSerializer(loan).data)
    return Response({"error": "No active loan found for this book."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def borrow_history(request, borrower_id):
    """
    List all books ever borrowed by the borrower, including return status.
    """
    borrower = get_object_or_404(Borrower, id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower)

    # Serialize the loan data to include both returned and unreturned books
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def borrowed_books(request, borrower_id):
    """
    List all active (unreturned) books for a borrower.
    """
    borrower = get_object_or_404(Borrower, id=borrower_id)
    active_loans = Loan.objects.filter(borrower=borrower, is_returned=False)

    # Serialize the active loan data
    serializer = LoanSerializer(active_loans, many=True)
    return Response(serializer.data)