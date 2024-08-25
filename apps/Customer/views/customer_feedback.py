
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.Customer.models.customer_feeback import CustomerFeedback
from apps.Customer.serializer import CustomerFeedbackSerializer

@api_view(['GET'])
def customer_feedback_list(request):
    """
    View to list all customer feedback.
    """
    feedbacks = CustomerFeedback.objects.all()
    serializer = CustomerFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def customer_feedback_create(request):
    """
    View to create new customer feedback.
    """
    serializer = CustomerFeedbackSerializer(data=request.data)
    service_id = request.data.get('service_id')

    if CustomerFeedback.objects.filter(service_id=service_id).exists():
        return Response({"detail": "Feedback for this service already exists."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def customer_feedback_detail(request, id):
    """
    View to retrieve a specific customer feedback.
    """
    try:
        feedback = CustomerFeedback.objects.get(id=id)
    except CustomerFeedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomerFeedbackSerializer(feedback)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def customer_feedback_update(request, id):
    """
    View to update a specific customer feedback.
    """
    try:
        feedback = CustomerFeedback.objects.get(id=id)
    except CustomerFeedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    
    partial = request.method == 'PATCH'
    
    # Only check service_id if it is included in the request data
    if 'service_id' in request.data and request.data['service_id'] != str(feedback.service_id.id):
        return Response({"detail": "Service ID cannot be changed."}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CustomerFeedbackSerializer(feedback, data=request.data, partial=partial)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def customer_feedback_delete(request, id):
    """
    View to delete a specific customer feedback.
    """
    try:
        feedback = CustomerFeedback.objects.get(id=id)
    except CustomerFeedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    
    feedback.delete()
    return Response({"detail": "Feedback deleted successfully."}, status=status.HTTP_204_NO_CONTENT)