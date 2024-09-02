
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.Customer.models.customer_feeback import CustomerFeedback
from apps.Customer.models.customer import Customer
from apps.Customer.serializer import CustomerFeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from apps.Customer.permissions.customer import  IsOwnCustomer
from django.views.decorators.csrf import csrf_exempt


#--------------------------------------------- FUNCTION BASED VIEW--------------------------------------------------------------------

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,IsOwnCustomer])
def feedback_list_or_create(request):
    """
    Retrieve a list of feedback for the authenticated user or create new feedback.
    """
    if request.method == 'GET':
        
        # Filter feedbacks for the authenticated user's services
        try:
            # Filter feedbacks for the authenticated user's services
            feedbacks = CustomerFeedback.objects.filter(service_id__customer=request.user.customer)
        except Customer.customer.RelatedObjectDoesNotExist:
            return Response({'message': 'No customer record found for this user.'}, status=status.HTTP_404_NOT_FOUND)
             
        
        if not feedbacks.exists():
            return Response({"detail": "No feedback found for your services."}, status=status.HTTP_200_OK)
        
        serializer = CustomerFeedbackSerializer(feedbacks, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CustomerFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the feedback with the service
            service_id = serializer.validated_data['service_id']
            if service_id.customer != request.user.customer:
                return Response({"detail": "You cannot provide feedback for this service."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnCustomer])
def feedback_detail(request):
    """
    Retrieve, update, or delete a specific feedback for the authenticated user.
    """
    feedback_id = request.data.get('id') if request.method in ['PUT', 'DELETE'] else request.query_params.get('id')
    
    if not feedback_id:
        return Response({"detail": "ID parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Retrieve the feedback object ensuring it belongs to the authenticated user
        feedback = CustomerFeedback.objects.get(id=feedback_id, service_id__customer=request.user.customer)
    except CustomerFeedback.DoesNotExist:
        return Response({"detail": "Feedback not found or you do not have permission to access this feedback."}, status=status.HTTP_404_NOT_FOUND)
    
    
    # Retrieve the feedback object ensuring it belongs to the authenticated user
    feedback = get_object_or_404(CustomerFeedback, id=feedback_id, service_id__customer=request.user.customer)
    
    if request.method == 'GET':
        serializer = CustomerFeedbackSerializer(feedback)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomerFeedbackSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        feedback.delete()
        return Response({"detail": "Feedback deleted successfully."}, status=status.HTTP_204_NO_CONTENT)