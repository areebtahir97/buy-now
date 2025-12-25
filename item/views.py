from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Item,Category
from .forms import NewItemForm,EditItemForm
# Create your views here.
#search
def items(request):
    query=request.GET.get('query','')       #get the query fron url
    categories=Category.objects.all()
    category_id=request.GET.get('category',0)
    items=Item.objects.filter(is_sold=False)
    
    if category_id:     #to filter based on category
        items=items.filter(category_id=category_id)
    
    if query:   #if query is present
        items=items.filter(Q(name__contains=query) | Q(description__icontains=query))    #filter to get the query only if name or dexcription contains it 
    
    return render(request,'item/items.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })

# for the item detail page
def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]     #get more objects from the same category excluding the current one
    return render(request,"item/detail.html",{
        'item':item,
        'related_items':related_items
    })
    
    #to be able to add new items
@login_required     #this means login is requeired
def new(request):
    if request.method=='POST':  #check if form is submitted
        form=NewItemForm(request.POST,request.FILES)
        
        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=request.user
            item.save()
            return redirect('item:detail',pk=item.id)
    form=NewItemForm()
    
    return render(request,'item/form.html',{
        'form':form,
      'title':'New Item' ,
    })
    
    #to delete item
@login_required
def delete(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()
    return redirect('dashboard:index')
  
#edit  
@login_required     #this means login is requeired
def edit(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    if request.method=='POST':  #check if form is submitted
        form=EditItemForm(request.POST,request.FILES,instance=item)     #instance=item mean this is for edit..so django wil not  create a new form
        
        if form.is_valid():
            form.save()
            return redirect('item:detail',pk=item.id)
    form=EditItemForm(instance=item)
    
    return render(request,'item/form.html',{
        'form':form,
      'title':'Edit Item' ,
    })

