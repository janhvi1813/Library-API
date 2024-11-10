# Library Management System API

## Project Overview

A Django REST API for managing books, borrowers, and loans in a library system.

## Setup Steps

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## API Endpoints

### Book Endpoints

- **POST** `/api/books/add/`: Add a new book.
- **GET** `/api/books/`: List all books. Filter by `?available=true`.

### Borrowing and Returning

- **POST** `/api/borrow/`: Borrow a book. Requires `book_id` and `borrower_id`.
- **POST** `/api/return/`: Return a book by `book_id`.

### Borrower History

- **GET** `/api/borrowed/<borrower_id>/`: List all active (unreturned) books for a borrower.
- **GET** `/api/history/<borrower_id>/`: List all books ever borrowed by the borrower, with return status.

## Business Rules

- A borrower must have an active membership (`is_active = True`) to borrow books.
- A borrower can borrow up to 3 books at a time.
- A book must be available (`available = True`) to be borrowed.

## Response Codes

- **201 Created**: Successfully created a resource.
- **403 Forbidden**: Borrowing not allowed due to inactive membership or exceeded limit.
- **400 Bad Request**: Book is unavailable or already loaned out.
- **404 Not Found**: Requested resource not found (e.g., no active loan found).

---

### Testing

Use tools like **Postman** or Django's built-in testing framework to test each endpoint and confirm that they adhere to the defined business rules and return appropriate status codes.

---

This setup should help you get your Django project running with proper organization, testing, and documentation. Let me know if you run into any issues!
