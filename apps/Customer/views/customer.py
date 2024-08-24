from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Customer.models import ServiceRequest
from apps.Customer.models import Customer
from apps.Customer.serializer import CustomerSerializer


# list all customer
@api_view(['GET'])
def list_customers(request):
   
    customers = Customer.objects.all()

   
    data = CustomerSerializer(customers, many=True)

    return Response(data.data, status=status.HTTP_200_OK)



# retrieve a single customer by ID
@api_view(['GET'])
def get_customer(request, id):
    try:
       
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

   
    data = CustomerSerializer(customer)

    return Response(data.data, status=status.HTTP_200_OK)


# create a new customer
@api_view(['POST'])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Update an existing customer
@api_view(['PUT'])
def update_customer(request, id):
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializer.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# Delete an existing customer
@api_view(['DELETE'])
def delete_customer(request, id):
    try:
        # Get the customer by ID
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    # Delete the customer
    customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)    