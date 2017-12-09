from django import forms
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SelectMultiple
from django.forms.extras.widgets import SelectDateWidget

# BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
CHOICES = (('1', 'accept'), ('2', 'decline'))
CATEGORY_CHOICE = (('e device','Electronic Device'),('Health&Beauty','Health & Beauty'), ('fashion', 'Fashion'), ('Sports', 'Sports'),
('Groceries', 'Groceries'), ('food','Food'), ('book', 'Book'), ('stationary', 'Stationary'),('others','Others')
)
# FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
#                             ('green', 'Green'),
#                             ('black', 'Black'))

class postForm(forms.Form):
    productname  = forms.CharField(required = True, max_length = 100)
    price = forms.FloatField(required = True)
    quantity = forms.IntegerField(required = True)
    category = forms.ChoiceField(required=True,
         widget=RadioSelect, choices=CATEGORY_CHOICE)
    description  = forms.CharField(required = True, max_length = 200, widget=forms.Textarea)
    pic = forms.FileField(required = True)

class OrderForm(forms.Form):
    message = forms.CharField(required = True, max_length = 250, widget=forms.Textarea)
    quantity = forms.IntegerField(required = True)
    # birth_year = DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # gender = ChoiceField(widget=RadioSelect, choices=GENDER_CHOICES)
    # favorite_colors = forms.MultipleChoiceField(required=False,
    #     widget=CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)

class conformationForm(forms.Form):
    Options = ChoiceField(widget=RadioSelect, choices=CHOICES)

class updateForm(forms.Form):

    new_price = forms.FloatField(required = True)
    new_quantity = forms.IntegerField(required = True)
    new_description  = forms.CharField(required = True, max_length = 200, widget=forms.Textarea)
