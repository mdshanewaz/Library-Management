from django.utils.timezone import now
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from BookApp.models import BookModel, BorrowModel
from BookApp.serializers import BookSerializer
from BookApp.permissions import IsAdminOrReadOnly

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        # Ensure only admins can update
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update books.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Ensure only admins can delete
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete books.")
        return super().destroy(request, *args, **kwargs)

class BorrowBookView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = BookModel.objects.get(id=book_id)
            borrow_book = BorrowModel.objects.filter(user=request.user, book=book_id)
        except BookModel.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)
        
        if book.amount <= 0:
            return Response({"error": "Book is not available for borrowing."}, status=400)
        
        if borrow_book:
            return Response({"error" : "You have already borrowed this book."}, status=404)
    
        borrowed_books_count = BorrowModel.objects.filter(user=request.user,  return_date__isnull=True).count()

        if borrowed_books_count == 5:
            return Response({"error": "You have reached the borrow limit of 5 books."}, status=400)

        BorrowModel.objects.create(user=request.user, book=book)
        book.amount -= 1
        book.save()

        return Response({
            "message": f"You have successfully borrowed '{book.name}'.",
            "return_deadline": (now() + timedelta(days=14)).strftime("%Y-%m-%d"),             
            }, status=200)

class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = BookModel.objects.get(id=book_id)
            borrow_record = BorrowModel.objects.get(user=request.user, book=book, return_date__isnull=True)
        except (BookModel.DoesNotExist, BorrowModel.DoesNotExist):
            return Response({"error": "No active borrow record found for this book."}, status=404)

        # Mark as returned
        borrow_record.return_date = now()
        borrow_record.save()

        book.amount += 1
        book.save()

        fine = borrow_record.fine

        return Response({
            "message": f"You have successfully returned '{book.name}'.",
            "fine": f"Your fine is {fine}"
            }, status=200)


class FineOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        borrows = BorrowModel.objects.filter(user=request.user, return_date__isnull=True)
        fines = [
            {
                "book_title": borrow.book.title,
                "borrow_date": borrow.borrow_date.strftime("%Y-%m-%d"),
                "return_deadline": (borrow.borrow_date + timedelta(days=14)).strftime("%Y-%m-%d"),
                "fine": borrow.fine,
            }
            for borrow in borrows
        ]

        total_fine = sum(fine["fine"] for fine in fines)

        if not total_fine:
            return Response({"message": "You have no fines."}, status=200)
        else:
            return Response({
                "fines": fines,
                "Total Fines" : total_fine
                }, status=200)
