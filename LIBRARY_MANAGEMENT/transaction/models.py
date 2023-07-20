from django.db import models
from book_management.models import Book, User
from datetime import datetime, timedelta
# Create your models here.


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='borrowed_books', on_delete=models.CASCADE)
    borrow_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_day = models.PositiveIntegerField(default=0)
    is_already_borrowed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'book']
    def __str__(self) -> str:
        return f'{self.user} borrowed {self.book}'
 
    def save(self, *args, **kwargs):
        if not self.borrow_date:
            self.borrow_date = datetime.now().date()

        if not self.return_date:
            self.return_date = self.borrow_date + timedelta(days=15)
        if self.return_date > self.borrow_date + timedelta(days=15):
            day_diff = (self.return_date - (self.borrow_date + timedelta(days=15))).days
            self.fine = day_diff * 5
            self.remaining_day = 0
        else:
            self.remaining_day = (self.borrow_date + timedelta(days=15) - self.return_date).days
            self.fine = 0 
        super().save(*args, **kwargs)
        
class Walet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.DecimalField(default=0,decimal_places=2,max_digits=20)