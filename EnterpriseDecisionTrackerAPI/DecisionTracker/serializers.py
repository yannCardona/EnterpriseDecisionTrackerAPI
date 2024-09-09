from rest_framework import serializers
from .models import Decision, Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Evaluation
        fields = ['user', 'goal_met', 'comments', 'evaluation_time']

class DecisionSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(many=True, read_only=True)  # Handle multiple evaluations

    class Meta:
        model = Decision
        fields = ['id', 'title', 'description', 'measurable_goal', 'status', 'evaluations']

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        # Remove the 'evaluations' field if it is empty
        if not representation['evaluations']:
            representation.pop('evaluations')
        return representation
