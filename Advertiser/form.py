from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.db.models import fields
from django.forms import Form
from django.forms.models import ModelForm
from .models import Advertisement_Create



class Advertisement_Form(ModelForm):
    class Meta:
        model = Advertisement_Create
        fields = ("Product_Name", "Product_Cost", "Product_Description", "Product_image","Is_Shipping")
        label = {

			"Product_Name": "Product Name",
			"Product_Cost": "Product Cost",
			"Product_Description": "Description",
			"Product_image":"Product Image",
   			"Is_Shipping": "Product Shipment"

		}
        
        
        
class Ad_Search(forms.Form):
    Search = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control mr-sm-2","placeholder":"Search Ads...","id":"tags"}))