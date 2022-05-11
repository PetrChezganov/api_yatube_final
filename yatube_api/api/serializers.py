from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    comments = serializers.StringRelatedField(
        many=True,
        read_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image', 'pub_date', 'group', 'comments')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        required=True,
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = (
            'id', 'user', 'following')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Такая подписка уже существует!')
            ),
        )

    def validate(self, data):
        user = self.context.get('request').user
        if user == data.get('following'):
            raise serializers.ValidationError(
                'Пользователь не может подписываться на самого себя!')
        return data
