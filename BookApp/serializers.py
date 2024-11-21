from rest_framework import serializers
from BookApp.models import BookModel

class BookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = BookModel
        fields = ['id', 'name', 'writer', 'amount', 'user']