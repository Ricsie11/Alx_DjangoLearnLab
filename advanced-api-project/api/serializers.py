from rest_framework import serializers
from .models import *
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__' #...To list all fields in the Author model


class BookSerializer(serializers.ModelSerializer): #...Used ModelSerializer for a fine grained CRUD experince
    author = AuthorSerializer(many=true, read_only=true) #...Nested AuthorSerializer to display author name within the book serializer
    class Meta:
        model = Book
        fields = '__all__' #....To list all fields in the Book model 

    def validate_publication_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError ("Publication year cannot be in the future.")
        return value
