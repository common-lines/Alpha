# Create your System - views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import signing
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime, timedelta, timezone
from django.db.models import Q, F, Sum, FloatField
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your "Core Forms" in views.
from .forms import (
    createuser, createproduct, craetimages, craetsize,
    craetcolors, craetpattern, clientupdate, reviewadd,
    postcreate, updatecore, createmessage, createrequest,
    updatestore, createinvoice, createloan, createmedia,
    updatemaincore, clientmainupdate
    )
# Create your "Core Table" in views.
from .models import (
    Product, vision, size, color, Client, pattern, review,
    Post, Message, Cart, Wishlist, Stipulate, Store, Vacate,
    Invoice, Prime, Contact, Lending, Movie, Explore, Promotion, 
    Search
    )
#models

# Create your views here.
def Home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def Products(request):
    realm = request.user.client.country
    province = request.user.client.region
    induct = request.user.client.institute
    boon = datetime.now()
    existing = boon.strftime("%Y-%m-%d")
    qs = Product.objects.filter(Q(location = realm ) | Q(location = province) | Q(location = induct)).order_by('-id').exclude(Q(active = False) | Q(terminate__lt = existing))
    paginator = Paginator(qs, 9)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #pagination code
    context = {
        'page' : posts,
    }
    return render(request, 'products.html', context)


@login_required(login_url='login')
def Checkout(request):
    user = request.user
    #Filter foreign key professional in QS
    # E.g: "seller__client__professinal = True"
    post1 = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).aggregate(sum_all=Sum('extent'))

    total_quantity = post1['sum_all']
    if total_quantity == None:
        total_quantity = 0
    #
    post12 = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).aggregate(total_price=Sum( F('extent') * F('product__price'), output_field=FloatField()))

    total_price =  post12['total_price']
    if total_price == None:
        total_price = 0
    #
    post = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).order_by('-pk')


    shepping = total_quantity * 5.0
    total_price_plus_shippind = shepping + total_price
    #
    context={
        'quatity': total_quantity,
        'price': total_price,
        'post' : post,
        'shepping' : shepping,
        'total_price_plus': total_price_plus_shippind,
    }
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def Profile(request):
    #user listing ends
    if request.user.client.subscription == "Titanium":
        existing = request.user.client.terminate +  timedelta(days = 5)
        #user days
        if request.user.client.duration == 90:
           curren = request.user.client.entirety
           day = 5 - curren
        elif request.user.client.duration == 30:
           curren = request.user.client.entirety
           day = 3 - curren
        else:
           curren = request.user.client.entirety
           day = 1 - curren
    elif request.user.client.subscription == "Platinum":
        existing = request.user.client.terminate +  timedelta(days = 3)
        #user days
        if request.user.client.duration == 30:
           curren = request.user.client.entirety
           day = 2 - curren
        else:
           curren = request.user.client.entirety
           day = 1 - curren
    else:
        existing = request.user.client.terminate +  timedelta(days = 2)
        #user days
        if request.user.client.duration == 30:
           curren = request.user.client.entirety
           day = 1 - curren
        else:
           curren = request.user.client.entirety
           day = 1 - curren
    #user message get
    user = request.user
    post = Post.objects.filter(Q(sender = user ) | Q(receiver = user)).order_by('-pk')
    #Core
    context = {
        'post': post,
        'existing': existing,
        'day' : day,
    }
    return render(request,'profile.html', context)

def Subscribe(request):
    return render(request, 'subscribe.html')

@login_required(login_url='login')
def Escape(request):
    logout(request)
    return redirect('home')

def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            error = "Provide Valid Credentials !!"
            context = {
                'error' : error
            }
            return render(request, 'core/login.html', context)

    context = {}
    return render(request, 'core/login.html', context)

def Register(request):
    form = createuser()

    if request.method == 'POST':
        form = createuser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            messages.success(request, 'Account Crated For \" ' + user + ' \"  Please Log In Bellow')
            return redirect('login')

    context = {'form' : form }

    return render(request, 'core/register.html', context)

@login_required(login_url='login')
def Blank(request):
    form = createinvoice()

    if request.method == 'POST':
        form = createinvoice(request.POST or None)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.user = request.user
            trans.spender = request.user
            trans.save()
            return redirect('profile')


    context = {
        'form' : form
    }
    return render(request, 'blank.html', context)


@login_required(login_url='login')
def Uplod(request):
    context = {
        'form': Product.objects.all()
    }
    return render(request, 'Uplod.html', context)



class Porductlist(ListView):
    model = Product
    template_name = 'Uplod.html'
    context_object_name = 'form'
    ordering = ['-pk']

class postdetails(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Product
    extra_context = {
        'list': reviewadd(),
        'form' : postcreate(),
    }

    def get_context_data(self, **kwargs):
        context = super(postdetails, self).get_context_data(**kwargs)
        qs = review.objects.filter(product = self.object).order_by('-pk')
        paginator = Paginator(qs, 3)
        #pagginate
        page = self.request.GET.get('page')
        #page_obj = paginator.get_page(p)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #pagination code
        context['item_list'] = posts
        return context


class productupload(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model =  Product
    form_class = createproduct

    def form_valid(self, form): #        'slug'
        if self.request.user.client.subscription == "Titanium":
            country = True
            zone = False
            institute = False
            if self.request.user.client.duration == 90:
                boon = datetime.now() +  timedelta(days = 90)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.country
                perimeter = 5
            elif self.request.user.client.duration == 30:
                boon = datetime.now() +  timedelta(days = 30)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.country
                perimeter = 3
            elif self.request.user.client.duration == 15:
                boon = datetime.now() +  timedelta(days = 15)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.country
                perimeter = 1
        elif self.request.user.client.subscription == "Platinum":
            country = False
            zone = True
            institute = False
            if self.request.user.client.duration == 30:
                boon = datetime.now() +  timedelta(days = 30)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.region
                perimeter = 2
            elif self.request.user.client.duration == 15:
                boon = datetime.now() +  timedelta(days = 15)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.region
                perimeter = 1
        elif self.request.user.client.subscription == "Silver":
            country = False
            zone = False
            institute = True
            if self.request.user.client.duration == 30:
                boon = datetime.now() +  timedelta(days = 30)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.institute
                perimeter = 1
            elif self.request.user.client.duration == 15:
                boon = datetime.now() +  timedelta(days = 15)
                existing = boon.strftime("%Y-%m-%d")
                spot = self.request.user.client.institute
                perimeter = 1


        while self.request.user.client.entirety < perimeter:
            form.instance.username = self.request.user
            form.instance.terminate = existing
            form.instance.active = False
            form.instance.country = country
            form.instance.zone = zone
            form.instance.institute = institute
            form.instance.location = spot
            form.instance.sample = self.request.POST.get('sample')
            form.instance.category = self.request.POST.get('category')
            form.instance.kind = self.request.POST.get('kind')
            form.instance.availability = self.request.POST.get('availability')
            super().form_valid(form)
            return redirect('mistakes')
        else:
            messages.success(self.request, 'Plase Subscribe T')
            return redirect('howler')

@login_required(login_url='login')
def Vision(request):
    queryset = Product.objects.filter(username = request.user ).last()
    cheker = queryset.active
    form = craetimages()
    if not cheker:
        queryset = Product.objects.filter(username = request.user ).last()
        queryset14 = queryset.vision
        form = craetimages()
        if request.method == 'POST':
            form = craetimages(request.POST or None, request.FILES or None, instance=queryset14 )
            if form.is_valid():
                form.save()
                return redirect('color')
    else:
        messages.success(request, 'Your Product Is Complite Activated!!')

    context = {
        'form' : form,
    }
    return render(request, 'core/mistakes.html', context)

@login_required(login_url='login')
def Color(request):
    queryset = Product.objects.filter(username = request.user ).last()
    cheker = queryset.active
    Size_form = craetsize() # queryset.size
    form = craetcolors() # queryset.color

    if not cheker:
        queryset = Product.objects.filter(username = request.user ).last()
        sizeform = queryset.size
        colorform = queryset.color
        Size_form = craetsize() # queryset.size
        form = craetcolors() # queryset.color
        if request.method == 'POST':
            Size_form = craetsize(request.POST, instance=sizeform )
            form = craetcolors(request.POST, instance=colorform )

            if Size_form.is_valid() and form.is_valid():
                updt = Size_form.save(commit=False)
                col = form.save(commit=False)
                updt.title = request.POST.get('size')
                col.title = request.POST.get('color')
                updt.save()
                col.save()
                return redirect('patten')
    else:
        messages.success(request, 'Your Product Is Complite Activated!!')


    context={
        'Size_form' : Size_form,
        'form' : form,
    }
    return render(request, 'core/colors.html', context)

@login_required(login_url='login')
def Howler(request):
    context={}
    return render(request, 'core/howler.html', context)

@login_required(login_url='login')
def Patten(request):
    queryset = Product.objects.filter(username = request.user ).last()
    cheker = queryset.active
    form = craetpattern()

    if not cheker:
        queryset = Product.objects.filter(username = request.user ).last()
        patter = queryset.pattern
        form = craetpattern()
        if request.method == 'POST':
            form = craetpattern(request.POST, instance=patter)
            if form.is_valid():
                form.save()
                return redirect('activate')
    else:
        messages.success(request, 'Your Product Is Complite Activated!!')


    context={
        'form' : form,
    }
    return render(request, 'core/pattens.html', context)

@login_required(login_url='login')
def Activate(request):
    queryset = Product.objects.filter(username = request.user ).last()
    cheker = queryset.active
    if not cheker:
        if request.method == 'POST':
            value = request.POST.get('true')
            if value == "emmanuel":
                #
                profile = Client.objects.filter(user = request.user).update(entirety = F('entirety') + 1)
                #.
                #
                queryset = Product.objects.filter(username = request.user ).last()
                queryset = Product.objects.filter(slug = queryset).update(active = True)
                #
                return redirect('listings')
    else:
        messages.success(request, 'Your Product Is Acivated')

    context={}
    return render(request, 'core/activate.html', context)

@login_required(login_url='login')
def Settings(request):

    form = clientupdate(request.POST or None, instance=request.user.client)
    U_form = updatecore(request.POST or None, instance=request.user)

    about = request.POST.get('about')

    if request.method == 'POST':
       form = clientupdate(request.POST or None, request.FILES or None, instance=request.user.client)
       U_form = updatecore(request.POST or None, instance=request.user)
       if form.is_valid() and U_form.is_valid():
           U_form.save()
           updt = form.save(commit = False)
           updt.about = about
           updt.save()
           messages.success(request, "Your Account Have Been Updated!!")
           return redirect('profile')


    context={
        'form' : form,
        'U_form' : U_form,
    }
    return render(request, 'profile/settings.html', context)

@login_required(login_url='login')
def Review(request, slug):
    #
    querset = Product.objects.get(slug = slug)
    rating = request.POST.get('rating')
    count = review.objects.filter(product = querset, author = request.user ).count()
    #
    if count <= 2:
        if request.method == 'POST':
            rating = request.POST.get('rating')
            if rating == None or int(rating) > 5:
                rating = 1
            else:
                pass

        if request.method == 'POST':
            form = reviewadd(request.POST or None)
            if form.is_valid():
                code = form.save(commit = False)
                code.author = request.user
                code.product = querset
                code.comment = request.POST.get('review')
                code.rating  = rating
                code.save()
                return redirect('listings')
    else:
        messages.success(request, "Account Crated For  Please Log In Bellow")

    context = {
        'rating': rating,
        'form' : slug,
        }

    return render(request, 'review.html', context)

@login_required(login_url='login')
def Message_In(request):
    form = postcreate(request.POST or None)
    receiver = request.POST.get('receiver')
    receiver = User.objects.get(username = receiver)

    subject = request.POST.get('subject')
    texting = request.POST.get('texting')
    sender = request.user

    postcount = Post.objects.filter(sender = sender, receiver = receiver, title = subject).count()

    if receiver == request.user:
        messages.success(request, 'I Dont Know How Your Able To do these, How can same person be sender ande receiver???, but it not goig to work')
    else:
        if postcount >= 1:
            messages.success(request, 'You Have started conservation with these user please check your inbox !!')
        else:
            if request.method == 'POST':
                form = postcreate(request.POST or None)
                mess = createmessage(request.POST)
                if form.is_valid():
                    code = form.save(commit=False)
                    code.sender = request.user
                    code.receiver = receiver
                    code.vendor = request.user
                    code.title = subject
                    code.save()
                    if mess.is_valid():
                        post = Post.objects.filter(sender = request.user).last()
                        cheker = mess.save(commit = False)
                        cheker.subject = post
                        cheker.receiver = receiver
                        cheker.vendor = request.user
                        cheker.texting = texting
                        cheker.save()
                        messages.success(request, 'Message Sent & Delivery!!')
                        return redirect('profile')
            else:
                return redirect('listings')

    context={
        'receiver' : receiver,
        'subject' : subject,
        'message' : texting,
        'sender' :  sender,
        'form': form,
    }
    return render(request, 'message/message.html', context)

@login_required(login_url='login')
def Contented(request, subject):
    qs = Post.objects.get(slug = subject)
    mess = Message.objects.filter(Q(receiver = request.user ) | Q(vendor = request.user), subject = qs)
    #Get core date
    subject = request.POST.get('subject')
    receiver = request.POST.get('receiver')
    texting = request.POST.get('texting')
    #main
    if request.method == 'POST':
        codemain = Post.objects.get(slug = subject)
        receiver = User.objects.get(username = receiver)
        form = createmessage(request.POST or None)
        if form.is_valid():
            texted = form.save(commit = False)
            texted.subject = codemain
            texted.receiver = receiver
            texted.vendor  = request.user
            texted.texting = texting
            texted.save()
            messages.success(request, 'Message Sent & Delivery!!')
        else:
            messages.warning(request, 'Message Dont delivery!!')

    context={
        'qs' : mess,
      }
    return render(request, 'messages.html', context)

@login_required(login_url='login')
def Mycart(request, slug):
    querset = Product.objects.get(slug = slug)
    #product catregory for advertising 
    main = querset.category
    #--/end
    cheker = Cart.objects.filter(user = request.user, product = querset ).count()
    if cheker >= 1:
        messages.success(request, 'Product Is Current In Your Shopping Cart !!')
    else:
        #update user advertise profile
        if request.user.promotion.category == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category = main)
        elif request.user.promotion.category2 == "None" :
            advertise = Promotion.objects.filter(user = request.user).update(category2 = main)
        elif request.user.promotion.category3 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category3 = main)
        elif request.user.promotion.category4 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category4 = main)
        elif request.user.promotion.category5 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category5 = main)
        else:
            advertise = Promotion.objects.filter(user = request.user).update(category6 = main)
       
        #end of  user update profile
        #use add to cart
        cats = Cart.objects.create(user = request.user, product = querset )
        
        if not cats:
            messages.success(request, 'Product Not Added To Your Shopping Cart!!')
        else:
            return redirect('viewcart')


    context={
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def Mywishlist(request, slug):
    querset = Product.objects.get(slug = slug)
    #product catregory for advertising 
    main = querset.category
    #--/end
    cheker = Wishlist.objects.filter(user = request.user, product = querset ).count()
    if cheker >= 1:
        messages.success(request, 'Product Is Current In Your Wish List !!')
    else:
        #update user advertise profile
        if request.user.promotion.category == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category = main)
        elif request.user.promotion.category2 == "None" :
            advertise = Promotion.objects.filter(user = request.user).update(category2 = main)
        elif request.user.promotion.category3 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category3 = main)
        elif request.user.promotion.category4 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category4 = main)
        elif request.user.promotion.category5 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(category5 = main)
        else:
            advertise = Promotion.objects.filter(user = request.user).update(category6 = main)
        #end of  user update profile
        wish = Wishlist.objects.create(user = request.user, product = querset )
        #main
        if not wish:
            messages.success(request, 'Product Not Added To Your WishList !!')
        else:
            return redirect('viewwish')

    context={
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def Viewcart(request):
    qs = Cart.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(qs, 6)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #pagination code

    context={
        'produc' : posts,
    }
    return render(request, 'profile/viewcart.html', context)

@login_required(login_url='login')
def Viewwish(request):
    qs = Wishlist.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(qs, 6)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #pagination code

    context={
        'produc' : posts,
    }
    return render(request, 'profile/viewwish.html', context)

@login_required(login_url='login')
def Delcart(request, slug):
    querset = Product.objects.get(slug = slug)
    cheker = Cart.objects.filter(user = request.user, product = querset ).count()

    if cheker < 1:
        messages.success(request, 'Product Is Current Delited In Your Shopping Cart !!')
    else:
        cats = Cart.objects.filter(user = request.user, product = querset ).delete()

        if not cats:
            messages.success(request, 'Product Is Not Delited In Your Shopping Cart!!')
        else:
            messages.success(request, ' Delited !!')
            return redirect('viewcart')

    context={
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def Delwish(request, slug):
    querset = Product.objects.get(slug = slug)
    cheker = Wishlist.objects.filter(user = request.user, product = querset ).count()

    if cheker < 1:
        messages.success(request, 'Product Is Current Delited In Your Shopping Cart !!')
    else:
        cats = Wishlist.objects.filter(user = request.user, product = querset ).delete()

        if not cats:
            messages.success(request, 'Product Is Not Delited In Your Shopping Cart!!')
        else:
            messages.success(request, ' Delited !!')
            return redirect('viewwish')

    context={
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def Request(request, slug):
    querset = Product.objects.get(slug = slug)
    #product location for advertising 
    country = querset.country
    zone = querset.zone
    institute = querset.institute
    current_price = querset.price
    #--/end
    #Request Post Seller
    seller = request.POST.get('seller')
    #Request Post Seller Get Forgenkey From Use Model
    receiver = User.objects.get(username = seller)
    #Request Quantity
    extent = request.POST.get('extent')
    #Request Verfication Codes
    unique = get_random_string(length=12, allowed_chars='QWERTYUIOPLKJHGFDSAZXCVBNM0987654321')
    #check if unique key available
    core = Stipulate.objects.filter(marked = unique).count()
    #change unique key
    if core >= 1:
        unique = get_random_string(length=32, allowed_chars='QWERTYUIOPLKJHGFDSAZXCVBNMabcdefghijklmnopqrstuvwxyz0987654321')
    #cod unique
    if request.user != receiver:
        if int(extent) <= 99 and int(extent) >= 1:
            #update user buying location
            if country == True:
                advertise = Promotion.objects.filter(user = request.user).update(country = F('country') + 1)
            elif zone == True:
                advertise = Promotion.objects.filter(user = request.user).update(zone = F('zone') + 1)
            elif institute == True:
                advertise = Promotion.objects.filter(user = request.user).update(institute = F('institute') + 1)
            else:
                pass
            #update user buying pricing avodation
            if current_price > request.user.promotion.maxmum:
                advertise = Promotion.objects.filter(user = request.user).update( maxmum = current_price)
                if advertise:
                    maxprice = current_price
                    minprice = request.user.promotion.minmum
                    current_average = (maxprice + minprice) / 2
                    advertise = Promotion.objects.filter(user = request.user).update( average = current_average)
            elif current_price < request.user.promotion.minmum:
                advertise = Promotion.objects.filter(user = request.user).update( minmum = current_price)
                if advertise:
                    maxprice = request.user.promotion.maxmum
                    minprice = current_price
                    current_average = (maxprice + minprice) / 2
                    advertise = Promotion.objects.filter(user = request.user).update( average = current_average)
            else:
                pass
            #end of advatising setup page
            form = createrequest(request.POST or None)
            if form.is_valid():
                chang = form.save(commit = False)
                chang.buyer = request.user
                chang.seller = receiver
                chang.product = querset
                chang.marked = unique
                chang.size = request.POST.get('size')
                chang.size01 = request.POST.get('size01')
                chang.color = request.POST.get('color')
                chang.color01 = request.POST.get('color01')
                chang.extent = request.POST.get('extent')
                chang.save()
                return redirect('orders')
            else:
                messages.success(request, 'Your Request Form Is Not Valid Please Try Again !!')
        else:
            messages.success(request, 'Please Change Your Order Request Quantity cant Be Greater Than 99 or 0 Include Negative Value!!')
    else:
        messages.success(request, 'What Your Try To DO.??, These Is Your Product You Cant Request It to Buy!!')
    context={
    }
    return render(request, 'request.html', context)


@login_required(login_url='login')
def Demand(request):
    user = request.user
    post12 = Stipulate.objects.filter(seller = user, terminate = False, admin = False, payment = False ).aggregate(total_price=Sum( F('extent') * F('product__price'), output_field=FloatField()  ))
    total_price =  post12['total_price']
    if total_price == None:
        total_price = 0
    #
    post = Stipulate.objects.filter(seller = user, terminate = False, admin = False, payment = False).order_by('-pk')
    #
    administrator = Stipulate.objects.filter(seller = user, admin = True, payment = True).order_by('-pk')
    #
    context={
        'price': total_price,
        'post' : post,
        'administrator' : administrator,
    }
    return render(request, 'profile/demend.html', context)

@login_required(login_url='login')
def Orders(request):
    user = request.user
    post1 = Stipulate.objects.filter(buyer = user, terminate = False, admin = False, payment = False).aggregate(sum_all=Sum('extent'))
    total_quantity = post1['sum_all']
    if total_quantity == None:
        total_quantity = 0
    #
    post12 = Stipulate.objects.filter(buyer = user, terminate = False, admin = False, payment = False).aggregate(total_price=Sum( F('extent') * F('product__price'), output_field=FloatField()  ))
    total_price =  post12['total_price']
    if total_price == None:
        total_price = 0
    #
    post = Stipulate.objects.filter(buyer = user, admin = False, payment = False).order_by('-pk')
    #
    administrator = Stipulate.objects.filter(buyer = user, admin = True, payment = True).order_by('-pk')
    #
    context={
        'quatity': total_quantity,
        'price': total_price,
        'post' : post,
        'administrator' : administrator,
    }
    return render(request, 'profile/orders.html', context)


@login_required(login_url='login')
def Shop(request, vessel):
    #Request Shop Owner
    owner = User.objects.get(username = vessel)
    posts = None
    #Get User Details
    realm = owner.client.professional
    #Check User If Is Subscribe To Profesinal
    if not realm and owner != request.user:
        messages.success(request, "These User Is Not Profesinal Seller You Can't View The Store!!")
        return redirect('profile')
    #Get Use Product Listed
    #Active Shop
    active_shop = owner.store.active
    #
    if active_shop == 'market':
        qs = Product.objects.filter(username =  owner ).order_by('-id').exclude(active = False)
        #Extrnal Data and ContextDectinary
        paginator = Paginator(qs, 6)
        #pagginate
        page = request.GET.get('page')
        #page_obj = paginator.get_page(p)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #pagination code
        context={'owner': owner, 'data' : posts }
        #context 
    elif active_shop == 'media':
        qs = Movie.objects.filter(user = owner).order_by('-id')
        paginator = Paginator(qs, 6)
        #pagginate
        page = request.GET.get('page')
        #page_obj = paginator.get_page(p)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #pagination code
        context={'owner': owner, 'media' : posts }
        #contex loan
         #context 
    elif active_shop == 'loan':
        qs = Lending.objects.filter(user = owner).order_by('-id')
        #
        paginator = Paginator(qs, 12)
        #pagginate
        page = request.GET.get('page')
        #page_obj = paginator.get_page(p)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #pagination code
        context={'owner': owner, 'loan' : posts }
        #contex loan

    return render(request, 'shop.html', context)

@login_required(login_url='login')
def Amend(request, vessel):
    #Request Shop Owner
    owner = User.objects.get(username = vessel)
    realm = owner.client.professional
    #Check User If Is Subscribe To Profesinal
    if owner != request.user:
        messages.success(request, "Hey What Are Your Try To Do, These Is Not Your Store You Cant Edit It.!!")
        return redirect('profile')
    else:
        if not realm:
            messages.success(request, "Please Subscribe To Professinal To Edit Your Store View.!!")
            return redirect('profile')
    form = updatestore(instance=request.user.store)
    if request.method == 'POST':
        form = updatestore(request.POST, request.FILES or None, instance=request.user.store)
        if form.is_valid():
            commi = form.save(commit=False)
            commi.active = request.POST.get('active')
            commi.save()
            messages.success(request, "Your Shop Have Been Updated!!")
            return redirect('profile')

    context={
        'form' : form,
     }
    return render(request, 'amend.html', context)


def Silver(request):
    context={
    }
    return render(request, 'plan/silver.html', context)
def Platinum(request):
    context={
    }
    return render(request, 'plan/platnum.html', context)
def Titanium(request):
    context={
    }
    return render(request, 'plan/titanium.html', context )

@login_required(login_url='login')
def Wallet(request):
    realm = request.user
    qs = Vacate.objects.filter(user = realm ).exclude(sent = True)
    #Transaction Id
    code_in = request.POST.get('transaction')
    if code_in == None:
        code = 'None'
    else:
        code_in = code_in.upper()
    #TUser Transaction Id
    get_invoice = Invoice.objects.filter(code = code_in).count()
    #Check If Transactio Exist
    if request.method == 'POST':
        if get_invoice < 1:
             messages.warning(request, "Transaction ID Donot exist!")
        else:
            test = Invoice.objects.get(code = code_in)
            if test.used == True:
                messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
            else:
                add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + test.value, mine = test.value)
                if add_prime:
                    test.spender = request.user
                    test.phone = request.user.client.phone
                    test.used = True
                    test.save()
                    messages.success(request, "You Have Regarge Your Wallet For " + str(test.value) + " Your Balance is Updated")

    context={
        'withdwar' : qs,
    }
    return render(request, 'profile/wallet.html', context )

@login_required(login_url='login')
def Withdraw(request):
    amaunt = request.POST.get('withdraw')
    #conver amount From str to Int
    amaunt_int = int(amaunt)
    realm = request.user.prime.value
    #Other Models
    via = request.POST.get('via')
    account = request.POST.get('account')
    #end model
    realm_user = request.user
    #Some Changes
    add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
    #Find User Total withdraw
    if add_withdwar['zoom'] == None:
        add_withdwar['zoom'] = 0
    #remove Pending withdwas from userwallet balance
    remain = realm - add_withdwar['zoom']
    #remain hold amount that user can withdwar
    if via == "none":
        messages.success(request, "Plase Select Method To Withdraw Cash From Your Wallet!")
    else:
        if amaunt_int < 2000:
            messages.success(request, "Plase Enter Withdraw Amount Greater Or Equal To 2000 !")
        else:
            if amaunt_int > realm:
                messages.success(request, "You Dont Have Insufficient Fund To Withdraw These Ammount!")
            else:
                if amaunt_int > remain:
                    messages.success(request, "You Hava Balance In Your Account, But Sum Of Pending Widthdraw Is Geater Than Your Balance!")
                else:
                    crear_order = Vacate.objects.create(user = request.user)
                    crear_order.amount = amaunt_int
                    crear_order.via = via
                    crear_order.account = account
                    crear_order.save()
                    messages.success(request, "We Have Receive Your Withdwar Order, We Will Paid Sholtly.!")
                    return redirect('wallet')
    #Error Redirect
    return render(request, 'profile/withdraw.html')

@login_required(login_url='login')
def Silver_Min(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 2000:
                if remain >= 2000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 2000, extract = 2000)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Silver"
                        user_update.duration = 15
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 2000:
                            remain = test.value - 2000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 2000, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Silver"
                                        user_update.duration = 15
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Silver"
                                    user_update.duration = 15
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/silvermin.html', context)



@login_required(login_url='login')
def Silver_Pro(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 3500:
                if remain >= 3500:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 3500, extract = 3500)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Silver"
                        user_update.duration = 30
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 3500:
                            remain = test.value - 3500
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 3500, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Silver"
                                        user_update.duration = 30
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Silver"
                                    user_update.duration = 30
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/silverpro.html', context)


@login_required(login_url='login')
def Platinum_Min(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 5000:
                if remain >= 5000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 5000, extract = 5000)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Platinum"
                        user_update.duration = 15
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 5000:
                            remain = test.value - 5000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 5000, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Platinum"
                                        user_update.duration = 15
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Platinum"
                                    user_update.duration = 15
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")

    context={
    }
    return render(request, 'plan/platinummin.html', context)

@login_required(login_url='login')
def Platinum_Pro(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 7000:
                if remain >= 7000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 7000, extract = 7000)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Platinum"
                        user_update.duration = 30
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 7000:
                            remain = test.value - 7000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 7000, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Platinum"
                                        user_update.duration = 30
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Platinum"
                                    user_update.duration = 30
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/platinumpro.html', context)

@login_required(login_url='login')
def Titanium_Min(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 7000:
                if remain >= 7000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 7000, extract = 7000)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Titanium"
                        user_update.duration = 15
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 7000:
                            remain = test.value - 7000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 7000, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Titanium"
                                        user_update.duration = 15
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Titanium"
                                    user_update.duration = 15
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/titaniummin.html', context )

@login_required(login_url='login')
def Titanium_Pro(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 9500:
                if remain >= 9500:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 9500, extract = 9500)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Titanium"
                        user_update.duration = 30
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 9500:
                            remain = test.value - 9500
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 9500, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Titanium"
                                        user_update.duration = 30
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Titanium"
                                    user_update.duration = 30
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/titaniumpro.html', context )

@login_required(login_url='login')
def Titanium_Enter(request):
    #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 25000:
                if remain >= 25000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 25000, extract = 25000)
                    if add_prime:
                        user_update = Client.objects.get(user = request.user)
                        user_update.subscription  = "Titanium"
                        user_update.duration = 90
                        user_update.terminate = datetime.now()
                        user_update.entirety = 0
                        user_update.save()
                        messages.success(request, "Thanks For Subscribe!")
                        return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 25000:
                            remain = test.value - 25000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 25000, mine = remain)
                                    if add_prime:
                                        user_update = Client.objects.get(user = request.user)
                                        user_update.subscription  = "Titanium"
                                        user_update.duration = 90
                                        user_update.terminate = datetime.now()
                                        user_update.entirety = 0
                                        user_update.save()
                                        messages.success(request, "Thanks For Subscribe!")
                                        return redirect('profile')
                            else:
                                test = Invoice.objects.filter(code = code_in).update(used = True)
                                if test:
                                    user_update = Client.objects.get(user = request.user)
                                    user_update.subscription  = "Titanium"
                                    user_update.duration = 90
                                    user_update.terminate = datetime.now()
                                    user_update.entirety = 0
                                    user_update.save()
                                    messages.success(request, "Thanks For Subscribe!")
                                    return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/titaniumenter.html', context )



@login_required(login_url='login')
def Professinal(request):
   #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 20000:
                if remain >= 20000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 20000, extract = 20000)
                    if add_prime:
                        profile = Client.objects.filter(user = request.user).update(professional = True)
                        if profile:
                            messages.success(request, "Thanks For Subscribe!")
                            return redirect('profile')
                else:
                     messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 20000:
                            remain = test.value - 20000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 20000, mine = remain)
                                    if add_prime:
                                        profile = Client.objects.filter(user = request.user).update(professional = True)
                                        if profile:
                                            messages.success(request, "Thanks For Subscribe!")
                                            return redirect('profile')
                                else:
                                    test = Invoice.objects.filter(code = code_in).update(used = True)
                                    if test:
                                        profile = Client.objects.filter(user = request.user).update(professional = True)
                                        if profile:
                                            messages.success(request, "Thanks For Subscribe!")
                                            return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/professinal.html', context )

@login_required(login_url='login')
def Erise_text(request, vessel):
    qs = Post.objects.get(slug = vessel)
    if request.method == 'POST':
        value = request.POST.get('true')
        if value == "emmanuel":
            #
            queryset = Post.objects.filter(slug = qs).delete()
            #
            return redirect('profile')
    context={
        'qs' : qs
    }
    return render(request, 'message/erasetext.html', context )

@login_required(login_url='login')
def Contact_In(request):
    queryset = Contact.objects.filter(user = request.user).order_by('-id')
    paginator = Paginator(queryset, 6)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #pagination code
    context={
        'qs' : posts,
    }
    return render(request, 'profile/contact.html', context )

@login_required(login_url='login')
def Contact_Out(request, vessel):
    receiver = User.objects.get(username = vessel)
    queryset = Contact.objects.filter(user = request.user, phone = receiver).delete()
    if queryset:
        return redirect('contact')

    return redirect('profile')

@login_required(login_url='login')
def Contact_Set(request, vessel):
    receiver = User.objects.get(username = vessel)
    queryset = Contact.objects.create(user = request.user, phone = receiver)
    if queryset:
        return redirect('contact')

    return redirect('profile')

@login_required(login_url='login')
def Listing(request):
    context={

    }
    return render(request, 'wring/listing.html', context )


@login_required(login_url='login')
def Loan_create(request):
    form = createloan()

    if request.user.client.subscription == "Titanium":
        if request.user.client.duration == 90:
            boon = datetime.now() +  timedelta(days = 90)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.country
            perimeter = 5
        elif request.user.client.duration == 30:
            boon = datetime.now() +  timedelta(days = 30)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.country
            perimeter = 3
        else:
            boon = datetime.now() +  timedelta(days = 15)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.country
            perimeter = 1

    elif request.user.client.subscription == "Platinum":
        if request.user.client.duration == 30:
            boon = datetime.now() +  timedelta(days = 30)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.region
            perimeter = 2
        else:
            boon = datetime.now() +  timedelta(days = 15)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.region
            perimeter = 1

    elif request.user.client.subscription == "Silver":
        if request.user.client.duration == 30:
            boon = datetime.now() +  timedelta(days = 30)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.institute
            perimeter = 1
        else:
            boon = datetime.now() +  timedelta(days = 15)
            existing = boon.strftime("%Y-%m-%d")
            spot = request.user.client.institute
            perimeter = 1

    if request.method == 'POST':
        form = createloan(request.POST or None, request.FILES or None)
        if form.is_valid():
            if request.user.client.entirety < perimeter:
                profile = Client.objects.filter(user = request.user).update(entirety = F('entirety') + 1)
                if profile:
                    core = form.save(commit=False)
                    core.user = request.user
                    core.terminate = existing
                    core.location = spot
                    core.save()
                    return redirect('loan')
            else:
                messages.success(request, 'Plase Subscribe T')
                return redirect('howler')
    context={
       'form' : form,
    }
    return render(request, 'wring/createloan.html', context )

@login_required(login_url='login')
def Loan(request):
    realm = request.user.client.country
    province = request.user.client.region
    induct = request.user.client.institute
    boon = datetime.now()
    existing = boon.strftime("%Y-%m-%d")
    qs = Lending.objects.filter(
        Q(location = realm ) |
        Q(location = province) |
        Q(location = induct)).order_by('-id').exclude(terminate__lt = existing)
    paginator = Paginator(qs, 9)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #pagination code
    context = {
        'page' : posts,
    }
    return render(request, 'wring/loan.html', context) #"core:base


@login_required(login_url='login')
def Loanbase(request, vessel):
    qs = Lending.objects.get(slug = vessel )
    context={
        'x' : qs
    }
    return render(request, 'wring/loanbase.html', context )


@login_required(login_url='login')
def Order_Delete(request, vessel):
    core = Stipulate.objects.get(marked = vessel)

    if core.buyer == request.user and core.admin == False and core.payment == False:
        delete =  core.delete()
        if delete:
            messages.success(request, 'Order Delited !!')
            return redirect('orders')
        else:
            return redirect('orders')
    else:
        return redirect('orders')

@login_required(login_url='login')
def Demand_Delete(request, vessel):
    core = Stipulate.objects.get(marked = vessel)
    existing = core.slot + timedelta(days=8)
    boon = datetime.now()

    existing = existing.strftime("%Y-%m-%d")
    boon = boon.strftime("%Y-%m-%d")

    if core.seller == request.user:
        if core.accepted == False or boon > existing and core.admin == False and core.payment == False:
            delete = Stipulate.objects.filter(marked = vessel).update(terminate = True)
            if delete:
                messages.success(request, 'Request Delited !!')
                return redirect('demand')
            else:
                return redirect('demand')
        else:
            messages.warning(request, 'You Have Agree To Sell You Can\'t delete, Please Contact Buyer For Eraise Of Order Or Waigth 8 dys for order expire')
            return redirect('demand')
    else:
        return redirect('demand')


@login_required(login_url='login')
def Vieworder(request, vessel):
    core = Stipulate.objects.get(marked = vessel)
    if core.terminate == False:
        if core.seller == request.user or core.buyer == request.user:
            objects = Stipulate.objects.get(marked = vessel)
        else:
            return redirect('home')
    else:
        return redirect('home')

    #user message get
    seller = core.seller
    buyer = core.buyer
    chats = Post.objects.filter(
         Q(Q(sender = seller ) | Q(receiver = seller)),
         Q(Q(sender = buyer ) | Q(receiver = buyer)) ).order_by('-pk')[:3]
    #Core
    #Delivary Adress
    seller_fulfillment = core.seller.client.institute
    loacations = Explore.objects.filter(emplacement = seller_fulfillment)[:4]
   
    
    #Delivary Adress

    #Mapbox token
    mapbox_access_token = 'pk.eyJ1IjoiY3liZXJnYXRlcyIsImEiOiJja2JlM2wyMWswaTViMnNuc2J2aDMwcHVsIn0.6b1wFLoqAu2KVoktBw58eA'
    #mapbox token
    context={
        'object' : objects,
        'chats' : chats,
        'mapbox_access_token' : mapbox_access_token,
        'loacations' : loacations,
    }
    return render(request, 'profile/vieworder.html', context) #"core:base

@login_required(login_url='login')
def Demand_Accepted(request, vessel):
    core = Stipulate.objects.get(marked = vessel)
    if core.seller == request.user and core.terminate == False:
        delete = Stipulate.objects.filter(marked = vessel).update(accepted = True)
        if delete:
            messages.success(request, 'Order Accepted !!')
            return redirect('demand')
        else:
            return redirect('demand')
    else:
        return redirect('demand')


@login_required(login_url='login')
def Shipping(request, vessel):
    sample = Stipulate.objects.get(marked = vessel)
    if sample.buyer == request.user and sample.terminate == False:
        if sample.accepted == True:
            unique = get_random_string(length=12, allowed_chars='QWERTYUIOPLKJHGFDSAZXCVBNM0987654321')
            #check if unique key available
            price = sample.extent * 5.0
            #price
            core = Stipulate.objects.filter(reference = unique).count()
            #change unique key
            if core >= 1:
                unique = get_random_string(length=32, allowed_chars='QWERTYUIOPLKJHGFDSAZXCVBNMabcdefghijklmnopqrstuvwxyz0987654321')
            main = Stipulate.objects.get(marked = vessel)
            main.shipping = True
            main.charge = price
            main.reference = unique
            main.save()
            messages.success(request, 'Order Can Be Shepped by admin !!')
            return redirect('orders')

        else:
            messages.success(request, 'You Cant shipp these order, Seller did not accept to sell, Please contact your seller for verfiction oforder !!')
            return redirect('orders')
    else:
        return redirect('orders')


@login_required(login_url='login')
def Shipping_Remove(request, vessel):
    sample = Stipulate.objects.get(marked = vessel)
    if sample.buyer == request.user and sample.terminate == False:
        if sample.accepted == True:
            delete = Stipulate.objects.filter(marked = vessel).update(shipping = False)
            if delete:
                messages.success(request, 'Remove Shepping Id !!')
                return redirect('orders')
            else:
                return redirect('orders')
        else:
            messages.success(request, 'You Cant shipp these order, Seller did not accept to sell, Please contact your seller for verfiction oforder !!')
            return redirect('orders')
    else:
        return redirect('orders')


@login_required(login_url='login')
def Orderprocess(request):
    user = request.user
    post1 = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).aggregate(sum_all=Sum('extent'))

    total_quantity = post1['sum_all']
    if total_quantity == None:
        total_quantity = 0
    #
    post12 = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).aggregate(total_price=Sum( F('extent') * F('product__price'), output_field=FloatField()))

    total_price =  post12['total_price']
    if total_price == None:
        total_price = 0
    #
    post = Stipulate.objects.filter(
        buyer = user, terminate = False,
        accepted = True, shipping = True).order_by('-pk')

    shepping = total_quantity * 5.0
    total_price_plus_shippind = shepping + total_price

    #Calculate and make payment with wallet
    realm = request.user.prime.value
    #end model
    realm_user = request.user
    #Some Changes
    add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
    if add_withdwar['zoom'] == None:
        add_withdwar['zoom'] = 0
    #remove Pending withdwas from userwallet balance
    remain = realm - add_withdwar['zoom']
    #remain hold amount that user can withdwar
    if realm >= total_price_plus_shippind:
        if remain >= total_price_plus_shippind:
            add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - total_price_plus_shippind, extract = total_price_plus_shippind)
            if add_prime:
                orders = Stipulate.objects.filter(
                    buyer = user, terminate = False,
                    accepted = True, shipping = True).update(shipping = False, admin = True, payment = True)
                if orders:
                    messages.success(request, "Thanks For Request shiiper Your Order(s), have been redeived")
                    return redirect('orders')
                else:
                    messages.success(request, "Is My Seen You dont have any shipping product")
                    return redirect('checkout')
        else:
            messages.success(request, "You Hava Balance In Your Account, But Total Babance minus Sum Of Pending Widthdraw, Remain is less than Order cost!")
            return redirect('checkout')
    else:
        messages.success(request, "You Dont Have Insufficient Fund  To Pay These order!")
        return redirect('checkout')

    context={
        'total_price_plus_shippind' : total_price_plus_shippind,
    }
    return render(request, 'profile/orderprocess.html', context) #"core:base

def Movies(request):
    form = createmedia()
    if request.method == 'POST':
        form = createmedia(request.POST or None, request.FILES or None )
        if form.is_valid():
            if request.user.client.software == True:
                core = form.save(commit=False)
                core.user = request.user
                core.location = request.user.client.institute
                core.terminate = request.user.client.ended
                core.category = request.POST.get('category')
                core.save()  
                return redirect('movielist')
            else:
                messages.success(request, "Plase subscribe to movies to list!")
        else:
            messages.success(request, "Form Securuty breached Please try again!")

    context = {
        'form' : form,
    }
    return render(request, 'wring/media.html', context)

@login_required(login_url='login')
def Movie_View(request):
    induct = request.user.client.institute
    incategory = "movie"
    boon = datetime.now()
    existing = boon.strftime("%Y-%m-%d")
    qs = Movie.objects.filter(location = induct, category = incategory ).order_by('-id').exclude(terminate__lt = existing)
    paginator = Paginator(qs, 9)
    #pagginate
    page = request.GET.get('page')
    #page_obj = paginator.get_page(p)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page' : posts,
    }
    return render(request, 'wring/movies.html', context)
    

@login_required(login_url='login')
def Movies_Details(request, vessel):
    core = Movie.objects.get(slug = vessel)
    #Core
    context={
        'x' : core,
    }
    return render(request, 'wring/moviedetails.html', context) #"core:base


@login_required(login_url='login')
def Movies_Software_Games(request):
   #Data Verfication
    if request.method == 'POST':
        wallet = request.POST.get('radio1')
        if wallet != None:
            #User balance
            realm = request.user.prime.value
            #end model
            realm_user = request.user
            #Some Changes
            add_withdwar = Vacate.objects.filter(user = realm_user).exclude(sent = True).aggregate(zoom = Sum('amount'))
            #Find User Total withdraw
            if add_withdwar['zoom'] == None:
                add_withdwar['zoom'] = 0
            #remove Pending withdwas from userwallet balance
            remain = realm - add_withdwar['zoom']
            #remain hold amount that user can withdwar
            if realm >= 7000:
                if remain >= 7000:
                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') - 7000, extract = 7000)
                    if add_prime:
                        # Dates
                        boon = datetime.now() +  timedelta(days = 29)
                        existing = boon.strftime("%Y-%m-%d")
                        #
                        profile = Client.objects.filter(user = request.user).update(software = True, ended = existing )
                        if profile:
                            messages.success(request, "Thanks For Subscribe!, Now You can list Movies, Software & Games For 29 days")
                            return redirect('profile')
                else:
                    messages.success(request, "You Hava Balance In Your Account, But  Total Babance minus Sum Of Pending Widthdraw Is Less Plan Prica!")
            else:
                messages.success(request, "You Dont Have Insufficient Fund To Subscribe These Plan!")

        elif wallet == None:
            code_get = request.POST.get('transaction')
            if code_get == None:
                code = None
            else:
                code_in = code_get.upper()
                #Get User Input
                get_invoice = Invoice.objects.filter(code = code_in).count()
                if get_invoice < 1:
                    messages.success(request, "Yout Transaction code do not exist!")
                else:
                    test = Invoice.objects.get(code = code_in)
                    if test.used == True:
                        messages.warning(request, "Transaction ID Is Oreday Used, Please Countact Us For More Details!")
                    else:
                        if test.value >= 7000:
                            remain = test.value - 7000
                            if remain >= 1:
                                test = Invoice.objects.filter(code = code_in).update(used = True, remain = remain )
                                if test:
                                    add_prime = Prime.objects.filter(user = request.user).update(value = F('value') + remain, extract = 7000, mine = remain)
                                    if add_prime:
                                        # Dates
                                        boon = datetime.now() +  timedelta(days = 29)
                                        existing = boon.strftime("%Y-%m-%d")
                                        #
                                        profile = Client.objects.filter(user = request.user).update(software = True, ended = existing )
                                        if profile:
                                            messages.success(request, "Thanks For Subscribe!, Now You can list Movies, Software & Games For 29 days")
                                            return redirect('profile')
                                else:
                                    test = Invoice.objects.filter(code = code_in).update(used = True)
                                    if test:
                                        # Dates
                                        boon = datetime.now() +  timedelta(days = 29)
                                        existing = boon.strftime("%Y-%m-%d")
                                        #
                                        profile = Client.objects.filter(user = request.user).update(software = True, ended = existing )
                                        if profile:
                                            messages.success(request, "Thanks For Subscribe!, Now You can list Movies, Software & Games For 29 days")
                                            return redirect('profile')
                        else:
                            messages.success(request, "These Trasaction dont have requred balance for plan price!")
    context={
    }
    return render(request, 'plan/mogasa.html', context )


@login_required(login_url='login')
def Mainsetting(request):
    form = clientmainupdate(request.POST or None, instance=request.user.client)
    U_form = updatemaincore(request.POST or None, instance=request.user)
    #
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone = request.POST.get('phone')
    institute = request.POST.get('institute')
    #
    if institute == 'iaa':
        region = 'Arusha'
        country = 'Tanzania'
    elif institute == 'mzumbe':
        region = 'Morogoro'
        country = 'Tanzania'
    elif institute == 'udom':
        region = 'Dodoma'
        country = 'Tanzania'
    else:
        institute == 'UNKNOWN'
        region = 'None'
        country = 'None'

    #
    if request.method == 'POST':
       form = clientmainupdate(request.POST or None, request.FILES or None, instance=request.user.client)
       U_form = updatemaincore(request.POST or None, instance=request.user)
        #
       if form.is_valid() and U_form.is_valid():
           updt = form.save(commit = False)
           updt.institute = institute
           updt.region = region
           updt.phone = phone
           updt.country = country
           updt.save()
           coreuser = U_form.save(commit = False)
           coreuser.first_name = first_name
           coreuser.last_name =last_name
           coreuser.save()
           messages.success(request, "Your Account Have Been Updated!!")
           return redirect('profile')
    return render(request, 'profile/settings.html')


def Search_View(request):
    query = request.GET.get('q', None)
    category = request.GET.get('category', None)
    #
    if request.user.is_authenticated:
        user = request.user
        location = request.user.client.institute
        Search.objects.create(user = user, query = query, location = location)
        main = str(query)
        category = str(category)
        #update user advertise profile
        if request.user.promotion.keyword == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword = main)
        elif request.user.promotion.keyword2 == "None" :
            advertise = Promotion.objects.filter(user = request.user).update(keyword2 = main)
        elif request.user.promotion.keyword3 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword3 = main)
        elif request.user.promotion.keyword4 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword4 = main)
        elif request.user.promotion.keyword5 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword5 = main)
        elif request.user.promotion.keyword6 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword6 = main)
        elif request.user.promotion.keyword7 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword7 = main)
        elif request.user.promotion.keyword8 == "None":
            advertise = Promotion.objects.filter(user = request.user).update(keyword8 = main)
        else:
            advertise = Promotion.objects.filter(user = request.user).update(keyword9 = main)
        #end of  user update profile
        Category7 = Promotion.objects.filter(user = request.user).update(category7 = category)


    context={
        'query' : query,
        'category' : category
    }
    return render(request, 'search/serchquery.html', context )
    