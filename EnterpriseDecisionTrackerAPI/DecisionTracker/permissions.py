from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class IsAdminGroupUser(BasePermission):

	def has_permission(self, request, view):
		# Check if the user belongs to the 'Admin' group
		return request.user.groups.filter(name='Admin').exists()