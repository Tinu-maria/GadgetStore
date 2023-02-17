from django import forms
from .models import Checkout
from .tasks import send_enquiry_email_task


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Username"})
    )
    email = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Email Address"})
    )
    password = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Password"})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Username"})
    )
    password = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Password"})
    )


class CartForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity ", widget=forms.NumberInput(attrs={'style': 'width:5ch', 'min': 1, 'max': 5})
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        exclude = ['user', ]

        widgets = {
            'address': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Address"}),
            'city' : forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your City"}),
            'state' : forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your State"}),
            'zipcode' : forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Zipcode"}),
            'phone_number' : forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Phone Number"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class EnquiryForm(forms.Form):
    email = forms.EmailField(
        label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Email Address"})
    )
    message = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter the query", "rows": 5})
    )

    def send_email(self):
        send_enquiry_email_task.delay(
            self.cleaned_data["email"], self.cleaned_data["message"]
        )  # Using .delay() we can send a task message quickly to Celery

        # send_feedback_email_task(
        #     self.cleaned_data["email"],self.cleaned_data["message"]
        # )
