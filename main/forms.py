from django import forms


# creating a form
class Button(forms.Form):
    sign = forms.BooleanField(initial=False, label='button')
