from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from products.models import Product

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        total_price = sum(item.product.price * item.quantity for item in items)
        data = {
            "items": [{"product": item.product.name, "price": item.product.price, "quantity": item.quantity} for item in items],
            "total_price": total_price,
        }
        return Response(data)

    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return Response({"message": "Product added to cart"})

    def delete(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"message": "Product removed from cart"})
