from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from apps.Customer.serializer.customer_service_request import ServiceRequestSerializer
from apps.Customer.models import ServiceRequest
from rest_framework.permissions import IsAuthenticated
from apps.Customer.permissions.customer import  IsOwnCustomer
from django.views.decorators.csrf import csrf_exempt

#--------------------------------------------- FUNCTION BASED VIEW--------------------------------------------------------------------


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,IsOwnCustomer])
def list_service_requests(request):
    
    user = request.user
    
    if request.method == 'GET':
        
        try:
            # Fetch service requests for the authenticated customer
            service_requests = ServiceRequest.objects.filter(customer=user.customer)
        except AttributeError:
            return Response({'error': 'User does not have an associated customer record.'}, status=status.HTTP_400_BAD_REQUEST)
        
       # service_requests = ServiceRequest.objects.all()
        
        if not service_requests.exists():
            
            return Response({'message': 'No service requests found for this user.'}, status=status.HTTP_200_OK)
        
        serializer = ServiceRequestSerializer(service_requests, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        
        serializer = ServiceRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnCustomer])
def service_request_detail(request):
    
    # Extract the service request id from the request data (POST body or query params)
    service_request_id = request.data.get('id') if request.method in ['PUT', 'PATCH', 'DELETE'] else request.query_params.get('id')
    
    if not service_request_id:
        return Response({'error': 'ID parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the service request ensuring it belongs to the authenticated customer
        service_request = ServiceRequest.objects.get(id=service_request_id, customer=request.user.customer)
    except ServiceRequest.DoesNotExist:
        return Response({'error': 'Service Request not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceRequestSerializer(service_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        
        if request.user.customer != service_request.customer:
            return Response({'error': 'You do not have permission to delete this service request.'}, status=status.HTTP_403_FORBIDDEN)
        
        service_request.delete()
        return Response({'message': 'Service request deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)