from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.Mechanic.models import Mechanic
from apps.Mechanic.serializer import MechanicSerializer




#---------------------------------------------CLASS BASED VIEW-----------------------------------------------------

class MechanicListCreateView(APIView):
    
    def get(self, request):
        mechanics = Mechanic.objects.all()
        serializer = MechanicSerializer(mechanics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MechanicSerializer(data=request.data)
        if serializer.is_valid():
            mechanic = serializer.save()
            return Response(MechanicSerializer(mechanic).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MechanicDetailView(APIView):
    def get(self, request, pk):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MechanicSerializer(mechanic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MechanicSerializer(mechanic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MechanicSerializer(mechanic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

        mechanic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)