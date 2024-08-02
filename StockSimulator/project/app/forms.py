from django import forms
from datetime import datetime

from .models import Stock, Event

class NewStockForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter stock name"}))
    price = forms.DecimalField(label="Price", decimal_places=2, max_digits=16, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter starting price"}))
    volatility = forms.DecimalField(label="Volatility", min_value=0, max_value=1, decimal_places=4, max_digits=16, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter volatility scale (between 0 and 1)"}))
    annualchange = forms.DecimalField(label="Annual Change", min_value=0, decimal_places=4, max_digits=16, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter average annual percentage change"}))


class AddStockForm(forms.Form):
    amount = forms.DecimalField(label="Amount", decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter amount"}))

    def __init__(self, user, **kwargs):
        super(AddStockForm, self).__init__(**kwargs)
        stocks = [(stock.id, stock.name) for stock in Stock.objects.filter(user=user)]
        self.fields['stock'] = forms.ChoiceField(label="Stock", choices=stocks, widget=forms.Select(attrs={'class': 'form-control'}))


class NewEventForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter event name"}))
    strength = forms.DecimalField(label="Strength", decimal_places=4, max_digits=16, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter strength (between -1 and 1)"}))
    decay_rate = forms.DecimalField(label="Decay Rate", decimal_places=4, max_digits=16, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter decay rate (between 0 and 1)"}))


class AddEventForm(forms.Form):
    def __init__(self, user, **kwargs):
        super(AddEventForm, self).__init__(**kwargs)

        events = [(event.id, event.name) for event in Event.objects.filter(user=user)]
        self.fields['event'] = forms.ChoiceField(label="Event", choices=events, widget=forms.Select(attrs={'class': 'form-control'}))

        current_date = datetime.today().strftime('%Y-%m-%d')
        in_year_date = str(int(current_date[:4]) + 1) + current_date[4:]
        self.fields['date'] = forms.DateField(label="Date", widget=forms.DateInput(attrs={'class': 'form-control', 'value': current_date, 'type': 'date', 'min': current_date, 'max': in_year_date}))