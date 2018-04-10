from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError


from .models import Item,List
from .forms import ItemForm, ExistingListItemForm
# Create your views here.
#def home_page(request):
#    return HttpResponse('<html><title>To-Do lists</title></html>')

def home_page(request):
    return render(request, 'home.html', {'form':ItemForm()})


def view_list(request, list_id):
    print('#######view_list#############')
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            #item = Item.objects.create(text=request.POST['text'], list=list_)
            return redirect('view_list', list_.id)
    return render(request, 'list.html', {'list': list_, "form": form})





def new_list(request):
    print('#######new_list#############')
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        #item = Item.objects.create(text=request.POST['text'], list=list_)
        return redirect('view_list', list_.id)
    else:
        return render(request, 'home.html', {"form": form})






