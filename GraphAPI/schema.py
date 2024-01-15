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
    
schema = graphene.Schema(query=Query)