from django_filters import rest_framework as filters
from .models import Decision

class DecisionFilter(filters.FilterSet):
	status = filters.CharFilter(field_name="status", lookup_expr='icontains')
	title = filters.CharFilter(field_name="title", lookup_expr='icontains')
	measurable_goal = filters.CharFilter(field_name="measurable_goal", lookup_expr='icontains')

	class Meta:
		model = Decision
		fields = ['status', 'title', 'measurable_goal']