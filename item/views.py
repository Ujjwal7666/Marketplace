import logging

from django.shortcuts import render ,redirect 
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from datetime import datetime
from django.core.files.base import ContentFile

from .models import Items, Category
# Create your views here.
logger = logging.getLogger('django')

def detail(request, pk):
    try:
        item = Items.objects.get(id=pk, is_sold =False)
        related_items = Items.objects.filter(category = item.category, is_sold=False).exclude(id=pk) [0:3]
        return render(request, 'item/detail.html', {'item':item, 'related_items':related_items}) 
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'item/detail.html', {'item':item, 'related_items':related_items})
    
@login_required
def new_item(request):
    try:
        categories = Category.objects.all()
        if request.method == 'POST':
            data = request.POST
            category_name = data.get('category')
            category =Category.objects.get(name= category_name)
            name = data.get('name') 
            description = data.get ('description')
            price = data.get('price')
            image = request.FILES.get('image')
            #  # Ensure image is not None and save it
            # if image:
            #     # Save image to MEDIA_ROOT using default_storage
            #     filename = default_storage.save(image.name, ContentFile(image.read()))
            Items.objects.create(category=category, name=name, description=description,price=price, image= image, created_by = request.user, created_at =datetime.now())
            return redirect ('index')
        return render(request, 'item/new_item.html', {'categories': categories} )
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'item/new_item.html', {'categories': categories} )
    
@login_required
def delete(request,pk):
    try:
        item = Items.objects.get(id =pk, created_by =request.user)
        item.delete()
        return redirect('userdashboard')
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return redirect('userdashboard')


@login_required
def edit_item(request,pk):
    try:
        categories = Category.objects.all()
        item = Items.objects.get(id =pk)
        if request.method == 'POST':
            data = request.POST
            category_name = data.get('category')
            category =Category.objects.get(name= category_name)
            name = data.get('name') 
            description = data.get ('description')
            price = data.get('price')
            is_sold = data.get('is_sold') == 'on'
            image = request.FILES.get('image')
             # Update fields
            item.category = category
            item.name = name
            item.description = description
            item.price = price
            item.is_sold = is_sold
            if image:  # Only update image if a new one is provided
                item.image = image
            item.created_by = request.user
            item.created_at = datetime.now()  # Using timezone.now() for current time
            item.save()

            # Items.objects.filter(id=pk).update(category=category, name=name, description=description,price=price, image= image, created_by = request.user, created_at =datetime.now())
            return redirect ('userdashboard')
        return render(request, 'item/update_item.html', {'categories': categories, 'item':item} )
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'item/update_item.html', {'categories': categories, 'item':item} )

def search(request):
    try:
        query = request.GET.get('q')
        results = []

        if query:
            results = Items.objects.filter(name__icontains=query)  # Adjust the filter as needed
            return render(request, 'item/search.html', {'results': results, 'query': query})
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'item/search.html', {'results': results, 'query': query})