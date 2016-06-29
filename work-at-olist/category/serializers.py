from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parents = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    subcategories = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Category
