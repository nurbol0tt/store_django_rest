from rest_framework import serializers

from product.models import Product, Rating, Comment, Category


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Comment
        fields = ("id", "user", "text", "children")


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("title", "image", "price",)


class ProductViewListSerializer(serializers.ModelSerializer):
    # pp = serializers.FloatField()

    class Meta:
        model = Product
        fields = ("title", "image", "price",)


class ProductMostPopularViewListSerializer(serializers.ModelSerializer):
    # pp = serializers.FloatField()

    class Meta:
        model = Product
        fields = ("title", "image", "price")


class ProductDetailSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field="title", read_only=True)
    color = serializers.SlugRelatedField(slug_field="title", read_only=True)
    category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    reviews = CommentSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    middle_star = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('id', 'middle_star', 'title', 'image', 'manufacturer', 'category', 'color',  'description',
                  'screen_size', 'processor_line', 'ram_size', 'drive_type', 'price', 'quantity',
                  'created', 'user', 'quantity', 'number_of_sales', 'likes', 'views', 'reviews', 'user',)


class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ('title', 'image', 'description', 'screen_size', 'processor_line',
                  'ram_size', 'drive_type', 'price', 'quantity', 'manufacturer', 'user', 'category', 'color')


class ProductUpdateSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Product
        exclude = ('likes', 'user', 'views', 'number_of_sales')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'image')


class ProductCategorySerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('text', 'product', 'user', 'parent')


class CreateRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ("star", "product")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            product=validated_data.get('product', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
