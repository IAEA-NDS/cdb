from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateMetaRecordSerializer


class CreateMetaRecordAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateMetaRecordSerializer(data=request.data)
        serializer.is_valid(True)
        meta_record = serializer.save()
        url = f"http://127.0.0.1:2500/cdbmeta/cdbrecord/json/{meta_record.pk}/"
        return Response({"url": url})
