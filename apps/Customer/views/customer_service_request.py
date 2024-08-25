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

# Retrieve a specific service request
@api_view(['GET'])
def get_service_request(request, id):
    try:
        
        service_request = ServiceRequest.objects.get(id=id)

    except ServiceRequest.DoesNotExist:
       
        return Response({'error': 'Service Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    serializer = ServiceRequestSerializer(service_request)
   
    return Response(serializer.data, status=status.HTTP_200_OK)
       

# Update a specific service request
@api_view(['PUT', 'PATCH'])
def update_service_request(request, id):
    try:
        # Retrieve the existing service request instance
        existing_service_request = ServiceRequest.objects.get(id=id)
    except ServiceRequest.DoesNotExist:
        return Response({'error': 'Service Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Initialize the serializer with the existing instance and new data
    serializer = ServiceRequestSerializer(instance=existing_service_request, data=request.data, partial=True)
    
    # Validate and save the serializer data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a specific service request
@api_view(['DELETE'])
def delete_service_request(request, id):
    try:
        service_request = ServiceRequest.objects.get(id=id)
    except ServiceRequest.DoesNotExist:
        return Response({'error': 'Service Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
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