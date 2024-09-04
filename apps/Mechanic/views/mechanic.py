from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from apps.Mechanic.permissions.mechanic import IsMechanicOrOwner
from apps.Mechanic.models import Mechanic
from apps.Mechanic.serializer import MechanicSerializer





#---------------------------------------------CLASS BASED VIEW-----------------------------------------------------

class MechanicListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the mechanic associated with the authenticated user
        try:
            # Retrieve the mechanic associated with the authenticated user
            mechanic = request.user.mechanic
        except Mechanic.DoesNotExist:
            return Response({"message": "No mechanic found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MechanicSerializer(mechanic)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MechanicSerializer(data=request.data)
        if serializer.is_valid():
            mechanic = serializer.save()
            return Response(MechanicSerializer(mechanic).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class MechanicDetailView(APIView):

  #  permission_classes = [IsAuthenticated, IsMechanicOrOwner]
    
   # def get(self, request, pk=None):
        # The mechanic can only access their own details
  #      mechanic = request.user.mechanic
        
   #     if not mechanic:
   #         return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
        
   #     serializer = MechanicSerializer(mechanic)
  #      return Response(serializer.data, status=status.HTTP_200_OK)

  #  def put(self, request, pk=None):
   #     mechanic = request.user.mechanic
        
   #     if not mechanic:
   #         return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

   #     serializer = MechanicSerializer(mechanic, data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_200_OK)
   #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   # def patch(self, request, pk=None):
     #   mechanic = request.user.mechanic
        
      #  if not mechanic:
      #      return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

      #  serializer = MechanicSerializer(mechanic, data=request.data, partial=True)
      #  if serializer.is_valid():
       #     serializer.save()
       #     return Response(serializer.data, status=status.HTTP_200_OK)
      #  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   # def delete(self, request, pk=None):
     #   mechanic = request.user.mechanic
        
      #  if not mechanic:
       #     return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)

       # mechanic.delete()
      #  return Response(status=status.HTTP_204_NO_CONTENT)