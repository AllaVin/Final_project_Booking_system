from rest_framework import generics
from apps.views_history.models.models import ViewHistory
from apps.views_history.serializers.serializers import ViewHistorySerializer

class ViewHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer

class ViewHistoryDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
