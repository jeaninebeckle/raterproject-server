"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import Categories


class Categories(ViewSet):


    def retrieve(self, request, pk=None):

        try:
            categories = Categories.objects.get(pk=pk)
            serializer = CategorySerializer(categories, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        categories = Categories.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Categories
        url = serializers.HyperlinkedIdentityField(
            view_name='categories',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')
