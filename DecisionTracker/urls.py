from django.urls import path
from .views import DecisionListCreate, DecisionRetrieveUpdateDestroy, evaluate_decision

urlpatterns = [
	path('decisions/', DecisionListCreate.as_view(), name='decision_list_create'),
	path('decisions/<int:pk>/', DecisionRetrieveUpdateDestroy.as_view(), name='decision_retrieve_update_destroy'),
	path('decisions/<int:pk>/evaluate/', evaluate_decision, name='evaluate_decision'),
]