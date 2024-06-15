from rest_framework import serializers
from .models import Startup, Rating, Comment, Category
from users.serializers import CustomUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StartupSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Startup
        fields = '__all__'


class StartupCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Startup
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'startup', 'value', 'created_at']


class CommentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at']


class CommentWriteSerializer(CommentBaseSerializer):
    class Meta(CommentBaseSerializer.Meta):
        pass


class CommentReadSerializer(CommentBaseSerializer):
    user = CustomUserSerializer(read_only=True)
    startup = StartupSerializer(read_only=True)

    class Meta(CommentBaseSerializer.Meta):
        fields = '__all__'


class TransactionSerializer(serializers.Serializer):
    startup_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The transaction amount must be positive.")
        return value
