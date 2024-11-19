from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework import status, mixins, viewsets, generics
from .serializers import  ImageSerializer, VideoSerializer, URLSerializer, TagSerializer, MetaKwordSerializer, TypeOfNewsSerializer
from attachments.models import Image, Video, URL, Tag, MetaKword, TypeOfNews
from .permissions import IsStaff, IsSupervisor, IsGetOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ImageModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name',]
    

class VideoModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name',]
    
    
class URLModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = URLSerializer
    queryset = URL.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name',]
    

class TagModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['confirm',]
    search_fields = ['name',]
    ordering_fields = ['name']


class TypeOfNewsModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = TypeOfNewsSerializer
    queryset = TypeOfNews.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name',]
    

class MetaKwordModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly|IsAdminUser]
    serializer_class = MetaKwordSerializer
    queryset = MetaKword.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name',]
    



class CheckIfTagIsConfirmedSView(APIView):
    """
    API endpoint to return tag's ID(if confirmed).
    """

    def get(self, request, tag_name):
        """
        Handles GET requests to retrieve a tag by name.

        Args:
            request: The incoming HTTP request object.
            tag_name: The name of the tag to retrieve.

        Returns:
            A JSON response containing the tag's ID (if confirmed)
            or an error message depending on the outcome.
        """

        try:
            tag = Tag.objects.get(name=tag_name)
            # logger.info(f"Successfully retrieved tag with name: {tag_name}")

            if tag.confirm:
                response_data = {
                    'message': 'Tag is confirmed',
                    'id': tag.id,
                }
                # logger.info(f"Returning confirmed tag details (ID: {tag.id}, name: {tag.name})")
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {'message': 'Tag exists but not confirmed'}
                # logger.info(f"Returning tag details (ID: {tag.id}, name not included as not confirmed)")
                return Response(response_data, status=status.HTTP_200_OK)

        except Tag.DoesNotExist:
            # logger.error(f"Tag with name {tag_name} not found")
            return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # logger.exception(f"An error occurred while retrieving tag: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

