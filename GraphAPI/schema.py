import graphene
import graphene_django
from django.contrib.auth.backends import UserModel
from django.db.models import Avg
from .models import Book, HasRead

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

offset = graphene.Int()
pagination_args ={
    'first': graphene.Int(default_value=10),
    'offset': offset
}
class Query(graphene.ObjectType):
    users = graphene.List(UserType, **pagination_args)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    books = graphene.List(BookType, fiction = graphene.Boolean(), **pagination_args)
    
    def resolve_books(self, info, **kwargs):
        fiction = kwargs.get('fiction')
        q = Book.objects.all()
        
        if fiction is not None:
            q = q.filter(fiction=fiction)
        
        return q
    
    def resolve_user(self, info, **kwargs):
        user_id = kwargs['id']
        return UserModel.objects.get(id=user_id)
    
    def resolve_users(self, info, **kwargs):
        first = kwargs.get('first')
        offset = kwargs.get('offset')
        
        q = UserModel.objects.all()
        
        return q[offset : offset+first]
    
class RateBookInput(graphene.InputObjectType):
    bookId = graphene.ID(required=True, name='book_id')
    userId = graphene.ID(required=True, name='user_id')
    rating = graphene.Int(required=True)

class RateBook(graphene.Mutation):
    class Arguments:
        input = RateBookInput(required=True)

    has_read = graphene.Field(HasReadType)

    def mutate(self, info, input):
        has_read_instance = HasRead()
        has_read_instances = has_read_instance.rate_book(input.bookId, input.userId, input.rating)
        return RateBook(has_read=has_read_instances)
    
class DeleteRating(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        
    query = graphene.Field(Query)
    
    def mutate(self, info, book_id, user_id):
        del_instance = HasRead()
        del_instance.delete_rating(book_id, user_id)
        return DeleteRating(query=Query)
    
            
            
class Mutation(graphene.ObjectType):
    rate_book = RateBook.Field()  
    delete_rating = DeleteRating.Field()     
    
schema = graphene.Schema(query=Query, mutation=Mutation)