from rest_framework import generics, status
from refbook.models import Refbook
from refbook.serializers import RefbookSerializer, RefbookElementSerializer
from refbook import utils
from rest_framework.response import Response
from rest_framework.views import APIView


class RefbookListView(generics.ListAPIView):
    serializer_class = RefbookSerializer

    def get_queryset(self):
        queryset = Refbook.objects.all()
        date = self.request.query_params.get('date')
        date = utils.convert_date(date)
        if date:
            queryset = queryset\
                .filter(versions__active_from__lte=date)\
                .distinct()
        
        return queryset

    def get(self, request, *args, **kwargs):
        date = self.request.query_params.get('date')
        if date:
            date = utils.convert_date(date)
            if not date:
                return Response(
                    data={'detail': 'Date has not valid format YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        response = super().get(request, *args, **kwargs)
        response.data['refbooks'] = response.data.pop('results')
        return response


class RefbookElementListView(generics.ListAPIView):
    serializer_class = RefbookElementSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        version = self.request.query_params.get('version')

        return utils.filter_elements(pk, version)

    def get(self, request, *args, **kwargs):
        try:
            Refbook.objects.get(id=kwargs['pk'])
        except Refbook.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response = super().get(request, *args, **kwargs)
        response.data['elements'] = response.data.pop('results')
        return response


class RefbookElementCheckView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            Refbook.objects.get(id=pk)
        except Refbook.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        version = self.request.query_params.get('version')
        element = RefbookElementSerializer(data=self.request.query_params.dict())
        if not element.is_valid():
            return Response(element.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = utils.filter_elements(pk, version)\
                .filter(**element.data)

        if queryset.exists():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
