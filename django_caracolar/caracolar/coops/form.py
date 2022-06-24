from django import forms



class DateInput(forms.DateInput):
    input_type = 'date'

class fechasForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    fecha_inicio = forms.DateField(label='Fecha de inicio', widget=DateInput)
    fecha_fin = forms.DateField(label='Fecha de fin', widget=DateInput)
