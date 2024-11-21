from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.models import User
from AuthApp.models import CustomUser

# Create your models here.
CATEGORY_CHOICES = ( 
    ("Story", "Story"), 
    ("SciFi", "SciFi"), 
    ("History", "History"), 
    ("Documentary", "Documentary"), 
    ("Comic", "Comic"), 
    ("Nobel", "Nobel"), 
    ("Religious", "Religious"), 
    ("Academic", "Academic"), 
) 

class BookModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    amount = models.PositiveIntegerField(default=1)
    added_to_library = models.DateTimeField(auto_now_add=True)

    borrowers = models.ManyToManyField(CustomUser, blank=True, through='BorrowModel', related_name='borrowed_books',)

    def __str__(self):
        return self.name

class BorrowModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.name}"
    
    @property
    def is_overdue(self):
        return not self.return_date and now() > self.borrow_date + timedelta(days=14)

    @property
    def fine(self):
        if self.return_date and self.return_date > self.borrow_date + timedelta(days=14):
            overdue_days = (self.return_date - (self.borrow_date + timedelta(days=14))).days
            return overdue_days * 5  # Fine rate: 5 BDT/day
        elif self.is_overdue:
            overdue_days = (now() - (self.borrow_date + timedelta(days=14))).days
            return overdue_days * 5
        return 0