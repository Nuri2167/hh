from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Vacancy
from .serializers import CompanySerializer, VacancySerializer

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class VacancyList(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class VacancyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class VacancyTopTen(generics.ListAPIView):
    queryset = Vacancy.objects.order_by('-salary')[:10]
    serializer_class = VacancySerializer

class CompanyVacancies(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        company_id = self.kwargs['id']
        return Vacancy.objects.filter(company_id=company_id)

@api_view(['POST'])
def submit_vacancy_application(request, id):
    vacancy = Vacancy.objects.get(id=id)
    # Send notification through channels
    return Response({'message': 'Application submitted successfully'}, status=status.HTTP_200_OK)

class SubmitApplicationView(APIView):
    def post(self, request, vacancy_id):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'vacancy_{vacancy_id}',
            {
                'type': 'send_notification',
                'message': 'New application submitted'
            }
        )
        return Response({'message': 'Application submitted'})

# Create your views here.
