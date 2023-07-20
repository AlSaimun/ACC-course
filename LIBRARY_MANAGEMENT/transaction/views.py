from django.shortcuts import render,redirect
from .models import Borrow,Book
from django.contrib import messages 
from django.db.models import Q
# Create your views here.

def borrow_book(request,isbn):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Book.objects.get(isbn=isbn)
    user = request.user
    borrow_obj = Borrow.objects.get_or_create(user=user,book=book)
    book.num_of_copies -= 1
    book.save()
    messages.success(request,"Borrowed Successfully")
    return redirect('transaction:show-borrow-book')
    

def show_borrowed_books(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    borrowed_books = Book.objects.filter(borrowed_books__user=user).distinct().exclude(isbn='').order_by('borrowed_books__return_date')
    return render(request, 'transaction/show_all_borrow_book.html', {'books': borrowed_books})  

def return_book(request, isbn):
    if not request.user.is_authenticated:
        return redirect('login') 
    try:
        borrow_obj = Borrow.objects.get(Q(book__isbn=isbn) & Q(user=request.user))
    except Borrow.DoesNotExist:
        return render(request, 'transaction/test.html', {'mes': "Borrow record not found"})
    
    print("print ", borrow_obj)
    if borrow_obj.fine > 0:
        borrow_obj.fine = 0.0
        borrow_obj.save()
        return render(request, 'transaction/pay_fine.html', {'fine': borrow_obj.fine})

    borrow_obj.delete()

    try:
        book = Book.objects.get(isbn=isbn)
        book.num_of_copies += 1
        book.save()
    except Book.DoesNotExist:
        return render(request, 'transaction/test.html', {'mes': "Book not found"})

    messages.success(request, "You Successfully Return book")
    return redirect('transaction:show-borrow-book')

def pay_fine(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
            messages.success(request, "You have successfully paid the fine.")
            return redirect('transaction:show-borrow-book')
    return render(request, 'book_management/pay_fine.html')

    
    
