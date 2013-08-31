from django.forms import ModelForm
from django.forms.models import modelform_factory


def formClassFactory(model, fields):
    ff = fields
    mm = model

    class formClass(ModelForm):
        class Meta:
            model = mm
            fields = ff
    return formClass
