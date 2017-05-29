from django import forms

# *****************************************************************************
class fNewPoiUser(forms.Form):
    poiUser = forms.CharField(label='Users Name', max_length=30)

