from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Item
from .forms import NewItemForm, EditItemForm
# Create your views here.


def items(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False)
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    
    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context = {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    }
    return render(request, 'item/items.html', context)
def detailPage(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    context = {'item': item, 'related_items': related_items,}
    return render(request, 'item/detail.html', context)
@login_required   
def newItem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id) #pk=item.id means we are passing the primary key (ID) of the newly created item to that URL.
    else:    
        form = NewItemForm()
    context = {"form": form, "title": 'New item'}
    return render(request, 'item/form.html', context)

@login_required
def deleteItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')
    

@login_required   
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id) #pk=item.id means we are passing the primary key (ID) of the newly created item to that URL.
    else:    
        form = EditItemForm(instance=item)
    context = {"form": form, "title": 'Edit item'}
    return render(request, 'item/form.html', context)


