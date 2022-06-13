from django import forms

class fechasForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    fecha_inicio = forms.DateField(label='Fecha de inicio')
    fecha_fin = forms.DateField(label='Fecha de fin')

