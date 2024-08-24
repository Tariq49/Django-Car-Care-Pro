from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Customer.serializer.customer_service_request import ServiceRequestSerializer
from apps.Customer.models import ServiceRequest

# List all service requests
@api_view(['GET'])
def list_service_requests(request):
    service_requests = ServiceRequest.objects.all()
    print(service_requests) 
    serializer = ServiceRequestSerializer(service_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve, update, or delete a specific service request
@api_view(['GET', 'PUT', 'DELETE'])
def get_service_request(request, id):
    try:
        service_request = ServiceRequest.objects.get(id=id)
    except ServiceRequest.DoesNotExist:
        return Response({'error': 'Service Request not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceRequestSerializer(service_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        service_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# create a new service request
@api_view(['POST'])
def create_service_requests(request):
    serializer = ServiceRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    