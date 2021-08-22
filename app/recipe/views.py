from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers

# Create a view set base it off generic viewset the LIST model mixin
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    "Manage tags in the database"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,) #this require that token authentication is used  and user is authenticated by API
    queryset = Tag.objects.all()  #when defining a list model mixin you need to  define the query set that you need to return
    serializer_class = serializers.TagSerializer

    #add a function that override the get quert set function
    def get_queryset(self):
        "Return objects for the current authenticated user only"
        #when it is call what happens when the list function is invoked  from URL, it will call
        #get_queryset to retireve Tag.objects  and this is where we can apply custom filtering like limit if to the authenticated user

        return self.queryset.filter(user=self.request.user).order_by('-name')
        #the req objects should be passed in to the self as a class varialbe
        #the user is assign to that because authentication is req
