from rest_framework import serializers
from core.models import Tag

class TagSerializer(serializers.ModelSerializer):
    "serializer fpr tag objects"
    #create a model serializer and link to tag model and pull in the ID and the name values

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)
