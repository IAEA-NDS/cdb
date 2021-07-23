from django.conf import settings
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateMetaRecordSerializer


class CreateMetaRecordAPI(APIView):
    def urls(self, meta_record_id):
        formats = ["json", "xml", "txt", "html"]
        urls = {}
        for file_format in formats:
            relative_url = reverse(
                f"cdbmeta:{file_format}", kwargs={"cdbrecord_id": meta_record_id}
            )
            urls[file_format] = f"{settings.SITE_ROOT_URL}{relative_url}"
        return urls

    def post(self, request, *args, **kwargs):
        serializer = CreateMetaRecordSerializer(data=request.data)
        serializer.is_valid(True)
        meta_record = serializer.save()
        response = {
            "detail": "Meta data saved into DB",
            "urls": self.urls(meta_record.pk),
        }
        return Response(data=response)
