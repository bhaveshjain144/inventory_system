from django.shortcuts import render
from rest_framework import generics, status
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if Item.objects.filter(name=request.data['name']).exists():
            return Response({'error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item = cache.get(f'item_{kwargs["pk"]}')
        if not item:
            try:
                item = Item.objects.get(pk=kwargs['pk'])
                cache.set(f'item_{kwargs["pk"]}', item)
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    # def get(self, request, *args, **kwargs):
    #     item = cache.get_or_set(f"item_{kwargs['pk']}", Item.objects.get(pk=kwargs['pk']))
    #     if not item:
    #         return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = self.get_serializer(item)
    #     return Response(serializer.data)
