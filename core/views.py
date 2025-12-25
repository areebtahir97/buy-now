from django.shortcuts import render,redirect
from item.models import Category, Item
from .forms import SignupForm

# Create your views here.

def index(request):
    items=Item.objects.filter(is_sold=False)[0:6]       #get 6 items which are not sold
    categories=Category.objects.all()
    return render(request,'core/index.html',{
        'categories':categories,
        'items':items,
    })

#for conatact
def contact(request):
    return render(request,'core/contact.html')

#create view for signup and pass intoo the frontend
def signup(request):
    if request.method=='POST':      #if the form has been submitted
        form=SignupForm(request.POST)   #get info from form
        if form.is_valid(): #if form is valid
            form.save() #then user will be created in db
            
            return redirect('/login/')
        
    else:  
        form=SignupForm()
    
    return render(request,'core/signup.html',{
        'form':form
    })