from django.forms import ModelForm
from django.db import models
from django import forms

# create user import
from Nile.models import (
     Invoice,
    )
# Create your form here.


class createinvoice(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude =  ['user','spender','remain','holder','used']

        

        
  
 