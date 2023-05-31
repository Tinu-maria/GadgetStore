from django.test import TestCase

# Create your tests here.

from django.forms import modelformset_factory
from flipkart_api.models import Product
from django.shortcuts import render, redirect


def modelformset_view(request):
    context ={}
  
    ProductFormSet = modelformset_factory(Product, fields =['name', 'price'])
    formset = ProductFormSet()
  
    context['formset']= formset
    return render(request, "product/formset.html", context)


def delete_modelformset_view(request):
    
    ProductFormSet = modelformset_factory(Product, fields =['name', 'price'])
    formset = ProductFormSet()
      
    if formset.is_valid():
        for form in formset:
            form.instance.delete()
            
    return render(request, "product/formsetdelete.html")



# ProductFormSet = modelformset_factory(Product, fields =['name', 'price'], can_delete=True)

# def modelformset_view(request):
#     formset = ProductFormSet(request.POST or None)
#     if request.method == 'POST' and formset.is_valid():
#         instances = formset.save(commit=False)
#         for instance in instances:
#             if instance.pk is None:
#                 instance.save()
#             elif instance.deleted:
#                 instance.delete()
#             else:
#                 instance.save()
#         formset.save_m2m()
#     return render(request, 'product/formset.html', {'formset': formset})


# MyModelFormSet = modelformset_factory(Product)

# formset = MyModelFormSet(request.POST or None)

# if request.method == 'POST' and 'delete' in request.POST:
#     form_index = int(request.POST.get('delete'))
#     form = formset.forms[form_index]

#     if form.is_valid():
#         instance = form.save(commit=False)

#         instance.delete() # delete the instance
        
#         formset.forms.pop(form_index) # delete form from the formset
        