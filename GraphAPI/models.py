from django.contrib.auth.backends import UserModel
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    fiction = models.BooleanField(default=False)
    description = models.TextField()
    published_year = models.IntegerField()
    
    def __str__(self) :
        return self.title
    
class HasRead(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='has_read')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='read_by')
    rating = models.IntegerField(null=True)
    
    class Meta:
        unique_together = ('user', 'book')
        
    def __str__(self):
        return f'{self.user.username} has read {self.book.title}'
    
    def rate_book(self, book_id, user_id, rating):
        try:
            book = Book.objects.get(id=book_id)
        except:
            ok = False
            raise Exception('Book with {book_id} does not exist')
        try:
            user = UserModel.objects.get(id=user_id)
        except:
            ok = False
            raise Exception('User with {user_id} does not exist')
        if rating < 0 or rating > 10:
            raise Exception('Rating must be between 0 and 10')
        
        has_read_intance, created = HasRead.objects.get_or_create(book=book, user=user)
        has_read_intance.rating = rating
        has_read_intance.save()
        return has_read_intance
    
    def delete_rating(self, book_id, user_id):
        try:
            book = Book.objects.get(id=book_id)
        except:
            ok = False
            raise Exception('Book with {book_id} does not exist')
        try:
            user = UserModel.objects.get(id=user_id)
        except:
            ok = False
            raise Exception('User with {user_id} does not exist')
        
        HasRead.objects.filter(user=user_id, book=book_id).delete()
