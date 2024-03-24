import boto3
from config import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):

        try:
            image_file = request.FILES['image']

            s3 = boto3.client('s3')
            s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, f'media/{image_file.name}')

            image_url = f"{settings.MEDIA_URL}{image_file.name}"
            return Response(data={'message': 'Image uploaded successfully', 'url': image_url}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

