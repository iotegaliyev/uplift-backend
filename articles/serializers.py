from rest_framework import serializers
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    tag_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), write_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'tags', 'tag_ids', 'created_at', 'views']
        read_only_fields = ['author']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids')
        article = Article.objects.create(**validated_data)
        article.tags.set(tag_ids)
        return article

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids')
        instance = super().update(instance, validated_data)
        instance.tags.set(tag_ids)
        return instance


