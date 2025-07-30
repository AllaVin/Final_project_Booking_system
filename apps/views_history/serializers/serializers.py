from rest_framework import serializers
from apps.views_history.models.models import ViewHistory

class ViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewHistory
        fields = '__all__'
