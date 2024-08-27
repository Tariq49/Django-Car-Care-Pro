
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.Customer.models.customer_feeback import CustomerFeedback
from apps.Customer.serializer import CustomerFeedbackSerializer



#--------------------------------------------- FUNCTION BASED VIEW--------------------------------------------------------------------

@api_view(['GET', 'POST'])
def feedback_list_or_create(request):
    """
    Retrieve a list of feedback or create a new feedback.
    """
    if request.method == 'GET':
        feedbacks = CustomerFeedback.objects.all()
        serializer = CustomerFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CustomerFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def feedback_detail(request, id):
    """
    Retrieve, update, or delete a specific feedback.
    """
    try:
        feedback = CustomerFeedback.objects.get(id=id)
    except CustomerFeedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomerFeedbackSerializer(feedback)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomerFeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
