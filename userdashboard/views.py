import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Items
# Create your views here.

logger = logging.getLogger('django')
@login_required
def userdashboard(request):
    try:
        items = Items.objects.filter(created_by = request.user)
        return render (request, 'userdashboard/userdashboard.html',{'items': items} )
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render (request, 'userdashboard/userdashboard.html',{'items': items} )

def dashboarddetail(request, pk):
    try:
        item = Items.objects.get(id=pk)
        related_items = Items.objects.filter(category = item.category).exclude(id=pk) [0:3]
        return render(request, 'userdashboard/dashboarddetail.html', {'item':item, 'related_items':related_items}) 
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'userdashboard/dashboarddetail.html', {'item':item, 'related_items':related_items}) 

