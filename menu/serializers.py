from rest_framework import serializers
from .models import MenuItem
from restaurants.models import Restaurant

class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    restaurant_url = serializers.HyperlinkedRelatedField(
        view_name="restaurant-detail",
        read_only=True,
        source="restaurant" 
    )

    class Meta:
        model = MenuItem
        fields = ['id','restaurant','restaurant_url', 'restaurant_name','name','price','available','created_at','updated_at']
        read_only_fields = ['id','restaurant_url','restaurant_name','created_at','updated_at']

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None
        instance = self.instance

        restaurant = attrs.get('restaurant')
        name = attrs.get('name').strip()
        price = attrs.get('price')

        if price <= 0:
            raise serializers.ValidationError({"price": "Price must be greater than zero!"})

        if not restaurant:
            raise serializers.ValidationError({"restaurant": "Restaurant is required."})
        
        if restaurant.owner != user:
            raise serializers.ValidationError({"restaurant": "Only restaurant owners can add menu items!"})

        if MenuItem.objects.filter(
            restaurant=restaurant, name__iexact=name
            ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError({"name": "This menu item already exists in this restaurant."})

        return attrs


    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if request and (not request.user.is_authenticated or request.user.role in ["customer", "delivery_agent"]):
            data.pop('created_at', None)
            data.pop('updated_at', None)

        return data
