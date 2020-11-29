"""View module for handling requests about designers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import Designer


class Designers(ViewSet):
    """Level up designers"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single designer

        Returns:
            Response -- JSON serialized designer
        """
        try:
            game_type = Designer.objects.get(pk=pk)
            serializer = DesignerSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all designers

        Returns:
            Response -- JSON serialized list of designers
        """
        designers = Designer.objects.all()

        serializer = DesignerSerializer(
            designers, many=True, context={'request': request})
        return Response(serializer.data)

class DesignerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for designers

    Arguments:
        serializers
    """
    class Meta:
        model = Designer
        url = serializers.HyperlinkedIdentityField(
            view_name='designer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')
