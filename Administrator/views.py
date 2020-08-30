from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime, timedelta
from django.db.models import Q, F, Sum
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
# Create your "Core Forms" in views.
# Create your views here.
from  django.contrib.auth.models import User
from  Nile.models import Invoice
#from django.contrib.auth.models import
from .forms import (
     createinvoice
    )
#

@staff_member_required(login_url='escape')
def Administrator(request):
    return render(request, 'administrator/core/index.html')

@staff_member_required(login_url='escape')
def Blank_Admin(request):
    receiver = User.objects.all().count()
    context = {
        'receiver' : receiver,
    }
    return render(request, 'administrator/pages/blank.html', context)

@staff_member_required(login_url='escape')
def Users_Admin(request):
    user = User.objects.all().order_by('-id')
    total = User.objects.all().count()
    context = {
        'users' : user,
        'total' : total,
    }
    return render(request, 'administrator/pages/users.html', context)

@staff_member_required(login_url='escape')
def Deposit_Admin(request):
    user = Invoice.objects.filter(user = request.user).order_by('-id')[:9]
    form = createinvoice()
    code = get_random_string(length=8, allowed_chars='QWERTYUIOPLKJHGFDSAZXCVBNM0987654321')
    codemax = request.POST.get('subject')
    if request.method == 'POST':
        form = createinvoice(request.POST)
        cheker = Invoice.objects.filter(code = codemax).count()
        print(cheker)
        if cheker >= 1:
            messages.warning(request, 'These Transaction Oreday Exist')
        else:
            if form.is_valid():
                trans = form.save(commit=False)
                trans.user = request.user
                trans.spender = request.user
                trans.code = codemax
                trans.save()
                messages.success(request, 'Sacessfull Transaction Creates!!')

    context = {
        'form' : form,
        'code' : code,
        'user' : user,
    }
    return render(request, 'administrator/pages/deposit.html', context)



