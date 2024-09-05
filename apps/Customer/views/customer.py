from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.Customer.models import Customer
from apps.Customer.serializer import CustomerSerializer
from apps.Customer.permissions.customer import  IsOwnCustomer
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt




#--------------------------------------------- FUNCTION BASED VIEW--------------------------------------------------------------------

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,IsOwnCustomer])

def customer_list_create(request):
    if request.method == 'GET':
        user = request.user
      
        customers = Customer.objects.filter(user=user)
       
        
        if not customers.exists():
            return Response({'message': 'No customers found for this user. Please ensure you are using the correct token or check if the user has any associated customers.'}, status=status.HTTP_200_OK)
        
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        
        user_id = request.data.get('user')
       
        if Customer.objects.filter(user=user_id).exists():
            return Response({'error': 'This user already has a customer record.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Save the customer without overriding the user field
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'unique_contact_number' in str(e):
                    return Response({'error': 'This contact number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'A database error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnCustomer])
def customer_detail(request):
    
    try:
        
        # Get the customer for the current user
        customer = Customer.objects.get(user=request.user)
        
    except Customer.DoesNotExist:
        
        if request.method == 'GET':
            return Response({'message': 'No customer record found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
     # Ensure the customer record belongs to the current user
    if customer.user != request.user:
        return Response({'error': 'You do not have permission to access this record.'}, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'GET':
        
        # Return the customer details
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        
        # Update the customer record
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        
        if serializer.is_valid():
            
            try:
                
                # Save the customer without overriding the user field
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except IntegrityError as e:
                
                if 'unique_contact_number' in str(e):
                    return Response({'error': 'This contact number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'A database error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        
        # Delete the customer record
        customer.delete()
        
        return Response({'message': 'Customer deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
  
     
    
