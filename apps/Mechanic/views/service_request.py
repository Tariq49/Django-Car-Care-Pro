from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.Customer.models import ServiceRequest
from apps.Customer.serializer.customer_service_request import ServiceRequestSerializer
from apps.Mechanic.permissions.mechanic import IsMechanicOrOwner
from apps.Mechanic.models import MechanicPricePerService



@api_view(['GET'])
@permission_classes([IsAuthenticated,IsMechanicOrOwner])
def mechanic_service_requests(request):
    """
    Retrieve all service requests assigned to the logged-in mechanic.
    Mechanics can only see their own requests.
    """
    try:
        # Access the mechanic profile via the user
        mechanic_profile = getattr(request.user, 'mechanic', None)
        
        # Ensure the user has a mechanic profile
        if not mechanic_profile:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        # Get the MechanicPricePerService instance
        mechanic_service = MechanicPricePerService.objects.filter(mechanic=mechanic_profile).first()

        if not mechanic_service:
            return Response({'detail': 'Mechanic service not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter service requests based on MechanicPricePerService instance
        service_requests = ServiceRequest.objects.filter(mechanic=mechanic_service)
        serializer = ServiceRequestSerializer(service_requests, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, IsMechanicOrOwner])
def update_service_request(request, pk):
    """
    Update a service request's mechanic_update, status, and completed_date.
    Mechanics can only update their own requests.
    """
    try:
        # Retrieve the service request
        service_request = ServiceRequest.objects.filter(pk=pk).first()

        if not service_request:
            return Response({'detail': 'Service request not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the logged-in user is authorized to update this request
        mechanic_profile = getattr(request.user, 'mechanic', None)
        if not mechanic_profile:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        mechanic_service = MechanicPricePerService.objects.filter(mechanic=mechanic_profile).first()
        if service_request.mechanic != mechanic_service:
            return Response({'detail': 'Not authorized to update this request'}, status=status.HTTP_403_FORBIDDEN)

        
       
        
        # Update fields if the user is authorized
        serializer = ServiceRequestSerializer(service_request, data=request.data, partial=True)
        
        if serializer.is_valid():
            
            updated_service_request = serializer.save()
            
            print('update service request-----------',updated_service_request)

            # Validate that completed_date can only be set if status is 'Completed'
            if updated_service_request.status == 'Completed':
                
                if not request.data.get('completed_date'):
                    return Response({'completed_date': 'This field is required when status is Completed.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                updated_service_request.completed_date = request.data.get('completed_date')
                
            elif updated_service_request.status in ['Pending', 'In Progress']:
                
                # Allow completed_date to be empty when status is 'Pending' or 'In Progress'
                if 'completed_date' in request.data and request.data.get('completed_date') is not None:
                    return Response({'error': 'You can only set completed_date when status is Completed.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                updated_service_request.completed_date = None
                
                
            if 'due_date' in request.data:
                updated_service_request.due_date = request.data.get('due_date')
            else:
                updated_service_request.due_date = service_request.due_date  

            
            updated_service_request.save()
            
            return Response(ServiceRequestSerializer(updated_service_request).data)
        
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)