from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from ..models import CostMainHead, CostSubHead

class SubCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostSubHead
        fields = ['id', 'name']


class GetSubHeadAPIView(ListAPIView):
    permission_classes= [AllowAny,]
    serializer_class = SubCodeSerializer
    queryset= CostSubHead.objects.filter()

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        queryset = queryset.filter(main_head_id=pk)
        return queryset