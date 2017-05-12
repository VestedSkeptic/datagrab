from __future__ import unicode_literals
from django.db import models

# *****************************************************************************
class mBase(models.Model):
    pass
    def __str__(self):
        return format("mBase")

    # -------------------------------------------------------------------------
    @staticmethod
    def getDictOfClassFieldNames(classModel):
        rvDict = {}
        fields = classModel._meta.get_fields()
        for field in fields:
            rvDict[field.name] = None
        return rvDict







