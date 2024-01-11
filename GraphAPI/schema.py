import graphene
import graphene_django
from django.contrib.auth.backends import UserModel
from django.db.models import Avg
from GraphAPI.models import Book, HasRead

class UserType(graphene_django.DjangoObjectType):
    average_rating = graphene.Float()
    
    def resolve_average_rating(self, info):
        query = self.has_read.all().aggregate(Avg('rating'))
        return query['rating__avg']
    
    class Meta(object):
        model = UserModel
        only_fields = ('id', 'username', 'has_read')
        
class BookType(graphene_django.DjangoObjectType):
    class Meta(object):
        model = Book
        
class HasReadType(graphene_django.DjangoObjectType):
    class Meta(object):
        model = HasRead

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    books = graphene.List(BookType)
    
    def resolve_books(self, info):
        return Book.objects.all()
    
    def resolve_users(self, info):
        return UserModel.objects.all()
    
schema = graphene.Schema(query=Query)