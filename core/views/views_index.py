import logging
from django.shortcuts import render
from django.views import View
from item.models import Items, Category

logger = logging.getLogger('django')
class index(View):

    def get(self, request):
        try:
            item = Items.objects.filter(is_sold = False)
            category = Category.objects.all()[0:6]
            return render (request, 'core/index.html', {'items': item, 'category': category})
        except Exception as exe:
            logger.error(str(exe),exc_info=True)
            return render (request, 'core/index.html', {'items': item, 'category': category})