from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Decision(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	measurable_goal = models.CharField(max_length=255)
	status = models.CharField(max_length=50, default="Pending", blank=True, null=True)

	def __str__(self):
		return self.title

class Evaluation(models.Model):
	decision = models.ForeignKey(Decision, related_name='evaluations', on_delete=models.CASCADE) 
	user = models.ForeignKey(User, related_name='evaluations', on_delete=models.CASCADE)  # User who made the evaluation
	goal_met = models.BooleanField()
	comments = models.TextField(blank=True, null=True)
	evaluation_time = models.DateTimeField(default=timezone.now, editable=False)  # Make the field non-editable

	def __str__(self):
		return f"Evaluation for {self.decision.title}"
