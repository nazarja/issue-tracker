from rest_framework.views import APIView
from rest_framework.response import Response


class ChartsAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ['Red', 'Blue', 'Yellow', 'Green']
        data = {
            'default': [10, 123, 52, 45],
            'labels': labels
        }
        return Response(data)
