from rest_framework import serializers
from .models import Decision, Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Evaluation
        fields = ['user', 'goal_met', 'comments', 'evaluation_time']

class DecisionSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(many=True, read_only=True)

    class Meta:
        model = Decision
        fields = ['id', 'title', 'description', 'measurable_goal', 'status', 'evaluations']

    # function to show the evaluations field of a decision only when not empty 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['evaluations']:
            representation.pop('evaluations')
        return representation
