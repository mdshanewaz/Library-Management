from django.urls import path
from rest_framework import routers
from BookApp.views import BookViewSet, BorrowBookView, ReturnBookView, FineOverviewView, BorrowedBooksDetailView, AvailableBookToBorrowView

router = routers.SimpleRouter()
router.register(r'list', BookViewSet)

app_name = 'BookApp'

urlpatterns = [
    path('<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('<int:book_id>/return/', ReturnBookView.as_view(), name='return_book'),
    path('fines/', FineOverviewView.as_view(), name='fine_overview'),
    path('borrow_details/', BorrowedBooksDetailView.as_view(), name='borrow_details'),
    path('available/', AvailableBookToBorrowView.as_view(), name="available_books"),
] + router.urls