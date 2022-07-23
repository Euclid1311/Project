from .models import Category,MainCategory,Sub_Category


def menu_links(request):
    links = MainCategory.objects.all()
    return dict(links=links)

def cat_menu_links(request):
    catlinks = Category.objects.all()
    return dict(catlinks=catlinks)


def sub_menu_links(request):
    sublinks = Sub_Category.objects.all()
    return dict(sublinks=sublinks)