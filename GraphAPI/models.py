from django.contrib.auth.backends import UserModel
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_year = models.IntegerField()
    
    def __str__(self) :
        return self.title
    
class HasRead(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='has_read')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='read_by')
    rating = models.IntegerField(null=True)
    
    class meta:
        unique_together = ('user', 'book')
        
    def __str__(self):
        return f'{self.user.username} has read {self.book.title}'