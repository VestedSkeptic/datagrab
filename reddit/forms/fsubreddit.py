from django import forms

# *****************************************************************************
class fNewPoiSubreddit(forms.Form):
    poiSubreddit = forms.CharField(label='Subreddit Name', max_length=30)

