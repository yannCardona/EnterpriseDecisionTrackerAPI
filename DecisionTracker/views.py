from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminGroupUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Decision
from .serializers import DecisionSerializer, EvaluationSerializer
from .filters import DecisionFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse

class DecisionPagination(PageNumberPagination):
	page_size = 1  # Set the default number of items per page
	page_size_query_param = 'page_size'  # Allow clients to specify page size via query param
	max_page_size = 10  # Set a limit on the maximum page size a client can request

@extend_schema(
	summary="List and create decisions",
	description=(
		"This endpoint allows users to list all decisions or create a new decision. "
		"Users need to be authenticated to create a decision, but listing decisions is available to all users."
	),
	tags=["decisions"],
	request=DecisionSerializer,
	responses={
		200: OpenApiResponse(
			description='List of decisions',
			examples={
				'application/json': [
					{
						'id': 1,
						'title': 'Decision 1',
						'description': 'Description of Decision 1',
						'measurable_goal': 'Goal 1',
						'status': 'Pending'
					},
					{
						'id': 2,
						'title': 'Decision 2',
						'description': 'Description of Decision 2',
						'measurable_goal': 'Goal 2',
						'status': 'Completed'
					}
				]
			}
		),
		201: OpenApiResponse(
			description='Decision created successfully',
			examples={
				'application/json': {
					'id': 3,
					'title': 'New Decision',
					'description': 'Description of the new decision',
					'measurable_goal': 'New goal',
					'status': 'Pending'
				}
			}
		),
		401: OpenApiResponse(description='Unauthorized'),
	}
)
class DecisionListCreate(generics.ListCreateAPIView):
	queryset = Decision.objects.all()
	serializer_class = DecisionSerializer
	pagination_class = DecisionPagination
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = DecisionFilter

@extend_schema(
	summary="Retrieve, update, or delete a decision",
	description=(
		"This endpoint allows users to retrieve, update, or delete a specific decision by its ID. "
		"Users need to be authenticated to update or delete a decision, while retrieving a decision is available to all users."
	),
	tags=["decisions/:id"],
	request=DecisionSerializer,
	responses={
		200: OpenApiResponse(
			description='Decision details',
			examples={
				'application/json': {
					'id': 1,
					'title': 'Decision 1',
					'description': 'Description of Decision 1',
					'measurable_goal': 'Goal 1',
					'status': 'Pending'
				}
			}
		),
		204: OpenApiResponse(description='Decision deleted successfully'),
		400: OpenApiResponse(description='Bad request'),
		401: OpenApiResponse(description='Unauthorized'),
		404: OpenApiResponse(description='Decision not found'),
	}
)
class DecisionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	queryset = Decision.objects.all()
	serializer_class = DecisionSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'put', 'delete']

@extend_schema(
	description=(
		"This endpoint allows users to evaluate a decision. Only decisions with the status 'Completed' can be evaluated."
		"Only Users from the 'Admin' Group can evaluate decisions."
	),
	summary="Evaluate a decision",
	tags=["evaluate"],
	request=EvaluationSerializer,
	responses={
		201: OpenApiResponse(
			description='Evaluation created successfully',
			examples={
				'application/json': {
					'title': 'Sample Decision Title',
					'description': 'Sample Description',
					'measurable_goal': 'Sample Goal',
					'status': 'Pending'
				}
			}
		),
		400: OpenApiResponse(description='Evaluation only allowed for completed decisions'),
		401: OpenApiResponse(description='Given token not valid for any token type'),
		403: OpenApiResponse(description='You do not have permission to perform this action'),
		404: OpenApiResponse(description='No Decision matches the given query')
	}
)
@api_view(['POST']) #only handle post requests
@permission_classes([IsAuthenticated, IsAdminGroupUser]) 
def evaluate_decision(request, pk):

	decision = get_object_or_404(Decision, pk=pk)

	if decision.status != 'Completed':
		return Response({'detail': 'Evaluation only allowed for completed decisions'}, status=status.HTTP_400_BAD_REQUEST)

	serializer = EvaluationSerializer(data=request.data)
	
	if serializer.is_valid():
		serializer.save(decision=decision, user=request.user)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)