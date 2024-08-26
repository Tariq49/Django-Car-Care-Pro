from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Mechanic.models import Mechanic
from apps.Mechanic.serializer import MechanicSerializer



@api_view(['GET', 'POST'])
def mechanic_list_create(request):
    if request.method == 'GET':
        mechanics = Mechanic.objects.all()
        serializer = MechanicSerializer(mechanics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = MechanicSerializer(data=request.data)
        if serializer.is_valid():
            mechanic = serializer.save()
            return Response(MechanicSerializer(mechanic).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def mechanic_detail(request, id):
    try:
        mechanic = Mechanic.objects.get(id=id)
    except Mechanic.DoesNotExist:
        return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MechanicSerializer(mechanic)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = MechanicSerializer(mechanic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        mechanic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
