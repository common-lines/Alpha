from django_summernote.widgets import SummernoteWidget, SummernoteWidgetBase,SummernoteInplaceWidget
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# create user import
from .models import (
     Product, Client, vision, size,
     color, pattern, review, Post,
     Message, Cart, Stipulate, Store,
     Invoice, Lending, Movie,
    )
# Create your form here.

class createuser(UserCreationForm):

    email = models.EmailField(verbose_name='email', max_length=255, unique=True)

    class Meta:
       model = User
       fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

# product forms

class createproduct(ModelForm):
    class Meta:
        model = Product
        fields = [
        'title',
        'price',
        'price_cancel',
        'description',
        'image'  ]

        widgets = {
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

class clientupdate(ModelForm):
    class Meta:
        model = Client
        fields= '__all__'
        exclude = ['user','subscription','duration','entirety','verified','adhere','professional','institute','region','country','institute']



class craetimages(ModelForm):
    class Meta:
        model  = vision
        fields = '__all__'
        exclude = ['product']



class craetsize(ModelForm):
    class Meta:
        model  = size
        fields = '__all__'
        exclude = ['product']


class craetcolors(ModelForm):
    class Meta:
        model  = color
        fields = '__all__'
        exclude = ['product']

class craetpattern(ModelForm):
    class Meta:
        model  = pattern
        fields = '__all__'
        exclude = ['product']


class reviewadd(ModelForm):
    class Meta:
        model = review
        fields = '__all__'
        exclude = ['author','product']


class postcreate(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['receiver','sender','vendor','slug']


class updatecore(ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class createmessage(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['subject','receiver','vendor']


class createrequest(ModelForm):
    class Meta:
        model = Stipulate
        fields = '__all__'
        exclude =  ['buyer','seller','product','marked','accepted','shipping','charge','reference','slot']


class updatestore(ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        exclude =  ['user']


class createinvoice(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude =  ['user','spender','remain','holder','used']


class createloan(ModelForm):
    loaninfo = forms.CharField(
        label='iframe',
        widget=SummernoteWidget( attrs={
            'summernote':
                    {'width': '100%',
                    'height': '300px',
                    'toolbar': [
                    ['style', ['style']],
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'height','paragraph']],
                    ['insert', ['link']],
                    ]
                }
           }
        )
    )

    collatexpl = forms.CharField(
        label='iframe',
         widget=SummernoteWidget( attrs={
            'summernote':
                    {'width': '100%',
                    'height': '300px',
                    'toolbar': [
                    ['style', ['style']],
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'height','paragraph']],
                    ['insert', ['link']],
                    ]
                }
           }
        )
    )

    loanrepay = forms.CharField(
        label='iframe',
        widget=SummernoteWidget( attrs={
            'summernote':
                    {'width': '100%',
                    'height': '300px',
                    'toolbar': [
                    ['style', ['style']],
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'height','paragraph']],
                    ['insert', ['link']],
                    ]
                }
           }
        )
    )

    wereap = forms.CharField(
        label='iframe',
         widget=SummernoteWidget( attrs={
            'summernote':
                    {'width': '100%',
                    'height': '300px',
                    'toolbar': [
                    ['style', ['style']],
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'height','paragraph']],
                    ['insert', ['link']],
                    ]
                }
           }
        )
    )

    class Meta:
        model = Lending
        fields = '__all__'
        exclude =  ['user','slug','terminate','location']

    def clean_document(self):
        cleaned_data = super(createloan, self).clean()
        media = cleaned_data.get('document')
        if media:
            filename = media.name
            if not filename.endswith('.pdf'):
                raise forms.ValidationError("Nots supportead")

        return media


class createmedia(ModelForm):
    requrement = forms.CharField(
        label='Requrement',
        widget=SummernoteWidget( attrs={
            'summernote':
                    {'width': '100%',
                    'height': '300px',
                    'toolbar': [
                    ['style', ['style']],
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'height','paragraph']],
                    ['insert', ['link','video']],
                    ]
                }
           }
        )
    )
    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ['user','slug','location','category','terminate']


class updatemaincore(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class clientmainupdate(ModelForm):
    class Meta:
        model = Client
        fields = ['phone','institute']









