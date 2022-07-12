from datetime import datetime, date

from django import forms
from .models import SolicitudCuidadosRecurrencia, SolicitudCuidadosFechas


class ControlFechaRecurrenciaForm(forms.ModelForm):
    class Meta:
        model = SolicitudCuidadosRecurrencia
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('horaInicio') is None:
             raise forms.ValidationError('La hora de incio debe ser completada')
        if self.cleaned_data.get('horaFin') is None:
             raise forms.ValidationError('La hora de fin debe ser completada')
        if self.cleaned_data.get('fecha') is None:
             raise forms.ValidationError('El dia debe ser completado')
        if self.cleaned_data.get('horaInicio') > self.cleaned_data.get('horaFin'):
            raise forms.ValidationError('La hora de incio debe ser anterior a la fecha de fin')
        if self.cleaned_data.get('fecha') < date.today():
            raise forms.ValidationError('La fecha no puede ser anterior a la fecha de hoy')

class ControlFechaFechasForm(forms.ModelForm):
    class Meta:
        model = SolicitudCuidadosFechas
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('horaInicio') is None:
             raise forms.ValidationError('La hora de incio debe ser completada')
        if self.cleaned_data.get('horaFin') is None:
             raise forms.ValidationError('La hora de fin debe ser completada')
        if self.cleaned_data.get('fecha') is None:
             raise forms.ValidationError('El dia debe ser completado')
        if self.cleaned_data.get('horaInicio') > self.cleaned_data.get('horaFin'):
            raise forms.ValidationError('La hora de incio debe ser anterior a la fecha de fin')
        if self.cleaned_data.get('fecha') < date.today():
            raise forms.ValidationError('La fecha no puede ser anterior a la fecha de hoy')
