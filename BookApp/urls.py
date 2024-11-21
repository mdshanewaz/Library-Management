from django.urls import path
from rest_framework import routers
from BookApp.views import BookViewSet, BorrowBookView, ReturnBookView

router = routers.SimpleRouter()
router.register(r'list', BookViewSet)

app_name = 'BookApp'

urlpatterns = [
    path('<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('<int:book_id>/return/', ReturnBookView.as_view(), name='return_book'),
] + router.urls