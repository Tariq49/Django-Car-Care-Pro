from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.Mechanic.models import MechanicPricePerService
from apps.Mechanic.serializer.price_per_service import MechanicPricePerServiceSerializer
from django.shortcuts import get_list_or_404


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mechanic_price_per_service_list(request):
    """
    list all mechanic prices per service records or create a new one.
    """
    if request.method =='GET':
        mechanic_id= request.query_params.get('mechanic_id')
        if mechanic_id:
            services = MechanicPricePerService.objects.filter(mechanic_id=mechanic_id)
        else:
            services = MechanicPricePerService.objects.all()

        serializer = MechanicPricePerServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    elif request.method =='POST':
        serializer = MechanicPricePerServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def mechanic_price_per_service_detail(request, pk):
    """
    Retrieve, update or delete a mechanic price per service record.
    """
    service = get_list_or_404(MechanicPricePerService, pk=pk)

    if request.method == 'GET':
        serializer = MechanicPricePerServiceSerializer(service)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MechanicPricePerServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
