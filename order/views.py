from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F
from product.models import Product


# Create your views here.

class BuyProductView(APIView):
    def post(self, request, product_id, format=None):
        try:
            # Get the product and acquire a select_for_update lock
            product = Product.objects.select_for_update().get(id=product_id)

            if product.stock > 0:
                # Reduce the stock by 1 and save the product inside a transaction
                with transaction.atomic():
                    product.stock = F('stock') - 1  # Decrement stock atomically
                    product.save()
                return Response({"message": "Product purchased successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Product is out of stock."}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
