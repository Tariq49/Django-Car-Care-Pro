from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from apps.Mechanic.models import MechanicPricePerService,Mechanic
from apps.Mechanic.serializer.price_per_service import MechanicPricePerServiceSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from apps.Mechanic.permissions.mechanic import IsMechanicOrOwner
from django.db import IntegrityError


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsMechanicOrOwner])
def mechanic_price_per_service_list(request):
    """
    list all mechanic prices per service records or create a new one.
    """
    
    mechanic = request.user.mechanic  # Get the authenticated mechanic

    if request.method == 'GET':
        # Filter services based on the authenticated mechanic
        services = MechanicPricePerService.objects.filter(mechanic=mechanic)
        
        if not services.exists():
            return Response({'message': 'No services found for this mechanic.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MechanicPricePerServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MechanicPricePerServiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(mechanic=mechanic)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "This service for the mechanic already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsMechanicOrOwner])
def mechanic_price_per_service_detail(request):
    """
    Retrieve, update or delete a mechanic price per service record.
    """
    mechanic = request.user.mechanic
    
    try:
        # Fetch the service that belongs to this mechanic
        service = MechanicPricePerService.objects.get(mechanic=mechanic)
    except MechanicPricePerService.DoesNotExist:
        return Response({'error': 'Mechanic price per service not found'}, status=status.HTTP_404_NOT_FOUND)

    # Object-level permission check
    request.user.check_object_permissions(request, service)

    if request.method == 'GET':
        serializer = MechanicPricePerServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MechanicPricePerServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
