
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import PropertyForm  # Создадим форму для работы с моделью

# Список недвижимости
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

# Создание недвижимости
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'property_form.html', {'form': form})

# Обновление недвижимости
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'property_form.html', {'form': form})

# Удаление недвижимости
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('property_list')
    return render(request, 'property_confirm_delete.html', {'property': property})

from django.shortcuts import render
def home(request):
    return render(request, 'home.html')

