from rest_framework import serializers

from products_api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


def validate_products_count(value: int) -> int:
    if value <= 0 or value >= 100:
        raise serializers.ValidationError("Значение должно быть больше 0 и меньше 100.")
    return value


class ParseViewSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(
        validators=[validate_products_count], default=10
    )
