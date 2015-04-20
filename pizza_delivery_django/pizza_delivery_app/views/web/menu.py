# coding: utf-8

from django.contrib.auth.decorators import login_required, permission_required
from pizza_delivery_app.methods.deviantsart import upload_image
from pizza_delivery_app.models import Company, Category, Product
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from pizza_delivery_app.models.venue import Venue, VenueProduct
from pizza_delivery_app.models.menu import SingleModifier, GroupModifier, GroupModifierItem, ModifierBinding, \
    GroupModifierBinding
from django.core.context_processors import csrf
from django import forms
import json


@login_required
def menu(request, venue_id):
    company = Company.get_by_username(request.user.username)
    if not company:
        return HttpResponseForbidden()
    try:
        venue = Venue.objects.get(id=venue_id)
        if venue.company != company:
            return HttpResponseForbidden()
    except Venue.DoesNotExist:
        return HttpResponseBadRequest()
    return redirect('/web/%s/menu/%s/category' % (venue_id, venue.first_category.id))


@login_required
@permission_required('pizza_delivery_app.read_categories')
@permission_required('pizza_delivery_app.read_products')
def category(request, venue_id, category_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        category = Category.objects.get(id=category_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        request_category = category
        while category.parent:
            category = category.parent
        if venue.first_category != category:
            return HttpResponseBadRequest()
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()
    values = {
        'venue_id': venue_id,
        'category': request_category,
        'children_categories': request_category.child.all(),
        'products': [product.venue_product.get(venue=venue) for product in request_category.product_category.all()],
        'status_map': dict(VenueProduct.STATUS_CHOICES),
        'create': request.user.has_perm('pizza_delivery_app.update_categories'),
        'update': request.user.has_perm('pizza_delivery_app.update_categories'),
        'delete': request.user.has_perm('pizza_delivery_app.update_categories'),
    }
    values.update(csrf(request))
    return render(request, 'web/menu/category.html', values)


class CategoryForm(forms.Form):
    parent_category_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    category_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u'Название', widget=forms.TextInput())
    description = forms.CharField(label=u'Описание', widget=forms.Textarea())
    image = forms.FileField(label=u'Картинка', widget=forms.ClearableFileInput(), required=False)


def save_category(form, venue):
    if form.cleaned_data['category_id']:
        category = Category.objects.get(id=form.cleaned_data['category_id'])
        category.name = form.cleaned_data['name']
        category.description = form.cleaned_data['description']
        if form.cleaned_data['image']:
            category.image_url = upload_image(form.cleaned_data['image'])
        category.save()
    else:
        category = Category(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                            parent=Category.objects.get(id=form.cleaned_data['parent_category_id']))
        category.save()
        if form.cleaned_data['image']:
            category.image_url = upload_image(form.cleaned_data['image'])
        category.save()
    category.get_first_category().save()


@login_required
@permission_required('pizza_delivery_app.create_categories')
def create_category(request, venue_id, category_id):
    def general_render(form):
        values = {
            'form': form,
            'venue_id': venue_id
        }
        values.update(csrf(request))
        return render(request, 'web/menu/category_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        category = Category.objects.get(id=category_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(CategoryForm(initial={
                'parent_category_id': category.id
            }))
        elif request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                save_category(form, venue)
                return redirect('/web/%s/menu/%s/category' % (venue_id, category_id))
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_categories')
def change_category(request, venue_id, category_id):
    def general_render(form):
        values = {
            'form': form,
            'venue_id': venue_id,
        }
        values.update(csrf(request))
        return render(request, 'web/menu/category_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        category = Category.objects.get(id=category_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(CategoryForm(initial={
                'parent_category_id': category.parent.id,
                'category_id': category_id,
                'name': category.name,
                'description': category.description
            }))
        elif request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                save_category(form, venue)
                return redirect('/web/%s/menu/%s/category' % (venue_id, category.parent.id))
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.delete_categories')
def delete_category(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        if request.method == 'POST':
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id=category_id)
            category.get_first_category().save()
            category.delete_category()
            return HttpResponse(json.dumps({
                'category_id': category_id
            }))
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


class ProductForm(forms.Form):
    category_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    product_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u'Название', widget=forms.TextInput())
    description = forms.CharField(label=u'Описание', widget=forms.Textarea())
    min_price = forms.IntegerField(label=u'Минимальная цена', widget=forms.NumberInput())
    image = forms.ImageField(label=u'Картинка', widget=forms.ClearableFileInput(), required=False)

    def hide_min_price(self):
        self.fields['min_price'].widget = forms.HiddenInput()
        self.fields['min_price'].label = u''
        self.fields['min_price'].required = False


def save_product(form, venue):
    if form.cleaned_data['product_id']:
        product = Product.objects.get(id=form.cleaned_data['product_id'])
        product.name = form.cleaned_data['name']
        product.description = form.cleaned_data['description']
        if form.cleaned_data['image']:
            product.image_url = upload_image(form.cleaned_data['image'])
        product.save()
    else:
        product = Product(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                          min_price=form.cleaned_data['min_price'],
                          category=Category.objects.get(id=form.cleaned_data['category_id']))
        product.save()
        if form.cleaned_data['image']:
            product.image_url = upload_image(form.cleaned_data['image'])
            product.save()
        product.save_in_venues(venue)
    product.category.get_first_category().save()


@login_required
@permission_required('pizza_delivery_app.create_products')
def create_product(request, venue_id, category_id):
    def general_render(form):
        values = {
            'form': form,
            'venue_id': venue_id
        }
        values.update(csrf(request))
        return render(request, 'web/menu/product_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        category = Category.objects.get(id=category_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(ProductForm(initial={
                'category_id': category.id
            }))
        elif request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                save_product(form, venue)
                return redirect('/web/%s/menu/%s/category' % (venue_id, category_id))
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_products')
def change_product(request, venue_id, product_id):
    def general_render(form):
        values = {
            'form': form,
            'venue_id': venue_id
        }
        values.update(csrf(request))
        return render(request, 'web/menu/product_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        product = Product.objects.get(id=product_id)

        if request.method == 'GET':
            form = ProductForm(initial={
                'category_id': product.category.id,
                'product_id': product.id,
                'name': product.name,
                'description': product.description
            })
            form.hide_min_price()
            return general_render(form)
        elif request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            form.hide_min_price()
            if form.is_valid():
                save_product(form, venue)
                return redirect('/web/%s/menu/%s/category' % (venue_id, product.category.id))
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.delete_products')
def delete_product(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            product.category.get_first_category().save()
            product.full_delete()
            return HttpResponse(json.dumps({
                'product_id': product_id
            }))
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_products')
def change_status(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'POST':
            venue_product_id = request.POST.get('venue_product_id')
            product = VenueProduct.objects.get(id=venue_product_id)
            product.change_status()

            return HttpResponse(json.dumps({
                'status': dict(VenueProduct.STATUS_CHOICES)[product.status],
                'product_id': venue_product_id
            }))
        else:
            HttpResponseNotAllowed(permitted_methods='POST')
    except VenueProduct.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_products')
def change_price(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        if request.method == 'POST':
            venue_product_id = request.POST.get('venue_product_id')
            product = VenueProduct.objects.get(id=venue_product_id)
            change = int(request.POST.get('change_in_price'))
            product.change_price(change)

            return HttpResponse(json.dumps({
                'price': product.price,
                'product_id': venue_product_id
            }))
        else:
            HttpResponseNotAllowed(permitted_methods='POST')
    except VenueProduct.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()
    except ValueError:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.read_single_modifiers')
@permission_required('pizza_delivery_app.read_group_modifiers')
def modifiers(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        group_modifiers = venue.group_modifiers.all()
        for modifier in group_modifiers:
            modifier.choices = modifier.group_modifier_item.all()
        return render(request, 'web/menu/modifiers.html', {
            'single_modifiers': venue.single_modifiers.all(),
            'group_modifiers': group_modifiers,
            'venue_id': venue.id,
            'create': request.user.has_perm('pizza_delivery_app.update_single_modifiers'),
            'update': request.user.has_perm('pizza_delivery_app.update_single_modifiers'),
            'delete': request.user.has_perm('pizza_delivery_app.update_single_modifiers')
        })
    except Company.DoesNotExist:
        return HttpResponseBadRequest()


class SingleModifierForm(forms.Form):
    single_modifier_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u'Название', widget=forms.TextInput())
    min_price = forms.IntegerField(label=u'Минимальная цена', widget=forms.NumberInput())
    image = forms.ImageField(label=u'Картинка', widget=forms.ClearableFileInput(), required=False)

    def hide_min_price(self):
        self.fields['min_price'].widget = forms.HiddenInput()
        self.fields['min_price'].label = u''
        self.fields['min_price'].required = False


def save_single_modifier(form, venue):
    if form.cleaned_data['single_modifier_id']:
        modifier = SingleModifier.objects.get(id=form.cleaned_data['single_modifier_id'])
        modifier.name = form.cleaned_data['name']
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
        modifier.save()
    else:
        modifier = SingleModifier(name=form.cleaned_data['name'], min_price=form.cleaned_data['min_price'])
        modifier.save()
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
            modifier.save()
        modifier.save_in_venues(venue)


@login_required
@permission_required('pizza_delivery_app.create_single_modifiers')
def create_single_modifier(request, venue_id):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/menu/modifier_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(SingleModifierForm())
        elif request.method == 'POST':
            form = SingleModifierForm(request.POST, request.FILES)
            if form.is_valid():
                save_single_modifier(form, venue)
                return redirect('/web/%s/menu/modifiers' % venue.id)
            else:
                return general_render(form)
    except Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_single_modifiers')
def change_single_modifier(request, venue_id, modifier_id):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/menu/modifier_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        modifier = SingleModifier.objects.get(id=modifier_id)

        if request.method == 'GET':
            form = SingleModifierForm(initial={
                'single_modifier_id': modifier.id,
                'name': modifier.name,
                'min_price': modifier.min_price
            })
            form.hide_min_price()
            return general_render(form)
        elif request.method == 'POST':
            form = SingleModifierForm(request.POST, request.FILES)
            form.hide_min_price()
            if form.is_valid():
                save_single_modifier(form, venue)
                return redirect('/web/%s/menu/modifiers' % venue.id)
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


class GroupModifierForm(forms.Form):
    group_modifier_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u'Название', widget=forms.TextInput())
    image = forms.ImageField(label=u'Картинка', widget=forms.ClearableFileInput(), required=False)


def save_group_modifier(form, venue):
    if form.cleaned_data['group_modifier_id']:
        modifier = GroupModifier.objects.get(id=form.cleaned_data['group_modifier_id'])
        modifier.name = form.cleaned_data['name']
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
        modifier.save()
    else:
        modifier = GroupModifier(name=form.cleaned_data['name'])
        modifier.save()
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
            modifier.save()
        modifier.save_in_venues(venue)


@login_required
@permission_required('pizza_delivery_app.create_single_modifiers')
def create_group_modifier(request, venue_id):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/menu/modifier_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(GroupModifierForm())
        elif request.method == 'POST':
            form = GroupModifierForm(request.POST, request.FILES)
            if form.is_valid():
                save_group_modifier(form, venue)
                return redirect('/web/%s/menu/modifiers' % venue.id)
            else:
                return general_render(form)
    except Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.update_single_modifiers')
def change_group_modifier(request, venue_id, modifier_id):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/menu/modifier_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        modifier = GroupModifier.objects.get(id=modifier_id)

        if request.method == 'GET':
            form = GroupModifierForm(initial={
                'group_modifier_id': modifier.id,
                'name': modifier.name
            })
            return general_render(form)
        elif request.method == 'POST':
            form = GroupModifierForm(request.POST, request.FILES)
            if form.is_valid():
                save_group_modifier(form, venue)
                return redirect('/web/%s/menu/modifiers' % venue.id)
            else:
                return general_render(form)
    except Category.DoesNotExist, Company.DoesNotExist:
        return HttpResponseBadRequest()


class GroupModifierItemForm(GroupModifierForm):
    group_modifier_item_id = forms.CharField(label=u'', widget=forms.HiddenInput(), required=False)
    min_price = forms.IntegerField(label=u'Минимальная цена', widget=forms.NumberInput())

    def hide_min_price(self):
        self.fields['min_price'].widget = forms.HiddenInput()
        self.fields['min_price'].label = u''
        self.fields['min_price'].required = False


def save_group_modifier_item(form, venue):
    if form.cleaned_data['group_modifier_item_id']:
        modifier = GroupModifierItem.objects.get(id=form.cleaned_data['group_modifier_item_id'])
        modifier.name = form.cleaned_data['name']
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
        modifier.save()
    else:
        modifier = GroupModifierItem(name=form.cleaned_data['name'], min_price=form.cleaned_data['min_price'])
        modifier.group_modifier = GroupModifier.objects.get(id=form.cleaned_data['group_modifier_id'])
        modifier.save()
        if form.cleaned_data['image']:
            modifier.image_url = upload_image(form.cleaned_data['image'])
            modifier.save()


@login_required
@permission_required('pizza_delivery_app.create_single_modifiers')
def create_group_modifier_item(request, venue_id):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/menu/modifier_form.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()

        if request.method == 'GET':
            return general_render(GroupModifierItemForm(initial={
                'group_modifier_id': request.GET.get('group_modifier_id')
            }))
        elif request.method == 'POST':
            form = GroupModifierItemForm(request.POST, request.FILES)
            if form.is_valid():
                save_group_modifier_item(form, venue)
                return redirect('/web/%s/menu/modifiers' % venue.id)
            else:
                return general_render(form)
    except Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def select_products_for_single_modifier(request, venue_id, modifier_id):
    def general_render():
        values = {
            'products': products,
            'modifier': modifier
        }
        values.update(csrf(request))
        return render(request, 'web/menu/select_products.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        modifier = SingleModifier.objects.get(id=modifier_id)
        bindings = ModifierBinding.objects.filter(modifier=modifier)
        binding_products = [binding.product for binding in bindings]
        if request.method == 'GET':
            products = venue.get_products_from_menu(venue_product=False)
            for product in products:
                product.has_modifier = product in binding_products
            return general_render()
        elif request.method == 'POST':
            for product in venue.get_products_from_menu(venue_product=False):
                confirmed = bool(request.POST.get(str(product.id)))
                if product in binding_products:
                    if not confirmed:
                        bindings[binding_products.index(product)].delete()
                else:
                    if confirmed:
                        ModifierBinding(product=product, modifier=modifier).save()
            return redirect('/web/%s/menu/modifiers' % venue.id)
    except Company.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def select_products_for_group_modifier(request, venue_id, modifier_id):
    def general_render():
        values = {
            'products': products,
            'modifier': modifier
        }
        values.update(csrf(request))
        return render(request, 'web/menu/select_products.html', values)

    try:
        venue = Venue.objects.get(id=venue_id)
        user_company = Company.get_by_username(request.user.username)
        if venue.company != user_company:
            return HttpResponseForbidden()
        modifier = GroupModifier.objects.get(id=modifier_id)
        bindings = GroupModifierBinding.objects.filter(modifier=modifier)
        binding_products = [binding.product for binding in bindings]
        if request.method == 'GET':
            products = venue.get_products_from_menu(venue_product=False)
            for product in products:
                product.has_modifier = product in binding_products
            return general_render()
        elif request.method == 'POST':
            for product in venue.get_products_from_menu(venue_product=False):
                confirmed = bool(request.POST.get(str(product.id)))
                if product in binding_products:
                    if not confirmed:
                        bindings[binding_products.index(product)].delete()
                else:
                    if confirmed:
                        GroupModifierBinding(product=product, modifier=modifier).save()
            return redirect('/web/%s/menu/modifiers' % venue.id)
    except Company.DoesNotExist:
        return HttpResponseBadRequest()