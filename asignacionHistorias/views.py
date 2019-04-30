from django.shortcuts import render
from rest_framework import viewsets, generics
from modelamientoAsignaciones import fabricaModelosLineales as fml, resolventes_genericos as rg



from .serializers import \
    AssignmentUniqueCostSerializer, \
    AssignmentWithAttributesSerializer, \
    AssignmentWithGroupsSerializer, \
    AssignmentWithPairsSerializer, \
    GeneratePairsSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class AssignmentUniqueCostView(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Return task assignment based in a unique cost input
        """
        data=request.data
        serializer = AssignmentUniqueCostSerializer( data=request.data)
        if serializer.is_valid():
            resultado_dict = fml.BalancedModelFactory(serializer.get_agents(), serializer.get_tasks()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentWithAttributesView(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True) 
    def post(self, request, format=None):
        """
        Return task assignment based in a unique cost input
        """
        data=request.data
        serializer = AssignmentWithAttributesSerializer( data=data)
        
        if serializer.is_valid():
            print(serializer.data)
            resultado_dict = fml.AttributeBasedModelFactory(serializer.get_agents(), serializer.get_tasks(), serializer.get_assign_same_quantity_of_tasks()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentWithGroupsView(APIView):
    permission_classes= (AllowAny, )
    @action(methods=['POST'], detail=True) 
    def post(self, request, format=None):
        """
        Return task assignment based in a unique cost input and groups of tasks
        """
        data = request.data
        serializer = AssignmentWithGroupsSerializer(data=data)
        if serializer.is_valid():
            resultado_dict = fml.TaskGroupModelFactory(serializer.get_agents(),  serializer.get_tasks(), serializer.get_groups()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DefaultAgentId(APIView):
    """
    Manage the default agent id used in the software
    """
    permission_classes = (AllowAny,)
    def get(self, reques):
        return Response({'default_id': rg.Agent.DEFAULT_ID})



class GeneratePairs(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True)
    def post(self, request):
        """
        Return agent pairs, can be similar in habilities or completely diferent
        """
        data = request.data
        serializer = GeneratePairsSerializer(data=data)
        if serializer.is_valid():
            resultado_dict = fml.PairMakerFactory(serializer.get_agents(),  serializer.get_reverse()).solve()
            print('resultado', resultado_dict)
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentByPairs(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True)
    def post(self, request):
        """
        Return task assignment, create the best pairs and assign task to the pairs
        """
        data = request.data
        serializer = AssignmentWithPairsSerializer(data=data)
        if serializer.is_valid():
            resultado_dict = fml.PairAssignmnentFactory(serializer.get_agents(), serializer.get_tasks(), serializer.get_reverse()).solve()
            print('resultado', resultado_dict)
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






