from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product, Category, User, Orders, Messages
from .forms import ProductForm, CategoryForm, MessageForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from telegrambot.views import send_message
from telegram.ext import CallbackContext
from telegram import Update
# Create your views here.


def login(request):
    return render(request, 'registration/login.html')


@login_required
def index(request):
    ctg = Category.objects.all().count()
    product = Product.objects.all().count()
    user = User.objects.all().count()
    orders = Orders.objects.all().count()
    return render(request, 'index.html', {'ctg': ctg, 'product': product, 'user': user, 'orders': orders, 's': True})


@login_required
def product_list(request):
    if request.POST:
        search = request.POST.get('search', '')
        products = Product.objects.filter(Q(ctg__name__icontains=search) | Q(name__icontains=search)).order_by('-pk')
        return render(request, 'product/list.html', {'products': products, 'search': search})
    products = Product.objects.all().order_by('-pk')
    return render(request, 'product/list.html', {'products': products})


@login_required
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product/details.html', {'product': product})


@login_required
def product_delete(request, pk=None):
    if pk:
        Product.objects.get(pk=pk).delete()
        messages.success(request, 'Product was successfully deleted')
        return redirect('product_list')

    return render(request, 'product/list.html')


@login_required
def product_add_edit(request, pk=None):
    try:
        instance = Product.objects.get(pk=pk)
    except:
        instance = None
    form = ProductForm(instance=instance)
    if request.POST:
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'product/forms.html', {'form': form})


@login_required
def category_list(request):
    if request.POST:
        search = request.POST.get('search', '')
        ctgs = Category.objects.filter(name__icontains=search).values().order_by('-pk')
        return render(request, 'category/list.html', {'ctgs': ctgs, 'search': search})
    ctgs = Category.objects.all().order_by('-pk')
    return render(request, 'category/list.html', {'ctgs': ctgs})


@login_required
def category_details(request, pk):
    ctg = Category.objects.get(pk=pk)
    return render(request, 'category/details.html', {'ctg': ctg})


@login_required
def category_delete(request, pk):
    if pk:
        Category.objects.get(pk=pk).delete()
        messages.success(request, 'Category was successfully deleted')
        return redirect('ctg_list')


@login_required
def category_add_edit(request, pk=None):
    try:
        instance = Category.objects.get(pk=pk)
    except:
        instance = None
    form = CategoryForm(instance=instance)
    if request.POST:
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('ctg_list')
    return render(request, 'category/forms.html', {'form': form})


@login_required
def message_list(request):
    msg = Messages.objects.all().order_by('-pk')
    return render(request, 'message/list.html', {'msgs': msg})


@login_required
def message_details(request, pk):
    msg = Messages.objects.get(pk=pk)
    return render(request, 'message/details.html', {'msg': msg})


@login_required
def message_delete(request, pk):
    if pk:
        Messages.objects.get(pk=pk).delete()
        messages.success(request, 'Message was successfully deleted')
        return redirect('message_list')


@login_required
def message_add(request, pk=None):
    form = MessageForm()
    if request.POST:
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('message_list')
    return render(request, 'message/forms.html', {'form': form})


@login_required
def order_list(request):
    if request.POST:
        search = request.POST.get('search', '')
        orders = Orders.objects.filter(Q(product__icontains=search) | Q(ctg__icontains=search)).values().order_by('-pk')
        return render(request, 'orders/list.html', {'orders': orders, 'search': search})
    orders = Orders.objects.all().order_by('-pk')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_delete(request, pk):
    if pk:
        Orders.objects.get(pk=pk).delete()
        messages.success(request, 'Order was successfully deleted')
        return redirect('order_list')


@login_required
def order_details(request, pk):
    order = Orders.objects.get(pk=pk)
    return render(request, 'orders/details.html', {'order': order})


@login_required
def user_list(request):
    if request.POST:
        search = request.POST.get('search', '')
        users = User.objects.filter(Q(name__icontains=search) | Q(phone_number__icontains=search) | Q(company_name__icontains=search)).values().order_by('-pk')
        return render(request, 'users/list.html', {'users': users, 'search': search})
    users = User.objects.all().order_by('-pk')
    paginator = Paginator(users, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/list.html', {'users': users, 'page_obj': page_obj})


@login_required
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'users/details.html', {'user': user})
