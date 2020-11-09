from django.db import models

class SerializableModel(models.Model):

    QPREFIX = ''

    class Meta:
        abstract = True

    @property
    def qualified_id(self):
        return self.QPREFIX + str(self.pk)
