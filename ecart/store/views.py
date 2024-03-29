


from pyexpat.errors import messages
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cartitem
from . models import Product, ProductGallery, ReviewRating
from category.models import MainCategory,Category,Sub_Category
from cart.models import Cartitem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

from .forms import ReviewForm
from django.contrib import messages


# Create your views here.

def store(request, main_category_slug=None,category_slug=None,sub_category_slug=None):
    main_categories = None
    categories      = None
    sub_categories  = None
    products        = None


    if main_category_slug != None:
        main_categories = get_object_or_404(MainCategory, slug=main_category_slug)
        products        = Product.objects.filter(main_category = main_categories, is_available=True)
        paginator     = Paginator(products,6)
        page          = request.GET.get('page')
        paged_products= paginator.get_page(page)
        product_count   = products.count()
        
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products   = Product.objects.filter(category = categories,is_available=True)
            paginator     = Paginator(products,6)
            page          = request.GET.get('page')
            paged_products= paginator.get_page(page)
            product_count=products.count()

            if sub_category_slug != None:
                sub_categories = get_object_or_404(Sub_Category,slug=sub_category_slug)
                products       = Product.objects.filter(sub_category = sub_categories,is_available=True)
                paginator     = Paginator(products,6)
                page          = request.GET.get('page')
                paged_products= paginator.get_page(page)
                product_count  = products.count()

    else:
        products      = Product.objects.all().filter(is_available=True).order_by('id')
        paginator     = Paginator(products,6)
        page          = request.GET.get('page')
        paged_products= paginator.get_page(page)
        product_count = products.count()
    main_category = MainCategory.objects.all()
    category = Category.objects.all()
    context = {
        'products': paged_products,
        'product_count' : product_count,
        'main': main_category,
        'category': category
    }
    return render(request, 'store/store.html',context)


def product_detail(request,main_category_slug,category_slug,sub_category_slug,product_slug):
    try:
        single_product = Product.objects.get(main_category__slug=main_category_slug ,category__slug=category_slug, sub_category__slug=sub_category_slug,slug=product_slug)
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)


    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html',context)



#search

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products        = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count   = products.count()
        context = {
            'products':products,
            'product_count':product_count,
            
        }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    print(url,"AAAAAAAAAAAaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
    if request.method == 'POST':

        try:
            reviews =ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form    =ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            print("last ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
            if form.is_valid():
                print(form,"===================================")
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                # data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id    = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted')
                return redirect(url)


