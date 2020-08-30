"""Alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
       path('', views.Home, name="home"),
       path('listings/', views.Products, name="listings"),
       path('checkout/', views.Checkout, name="checkout"),
       path('profile/', views.Profile, name="profile"),
       path('pricing/', views.Subscribe, name="subscribe"),
       path('login/', views.Login,  name="login"),
       path('register/', views.Register, name="register"),
       path('quit/', views.Escape, name="escape" ),
       path('blank/', views.Blank, name="blank"),
       path('uplod/new/', views.productupload.as_view(), name="product-create"),
       path('post/<str:slug>/', views.postdetails.as_view(), name="product-detail"),
       path('images/', views.Vision, name="mistakes"),
       path('colors/', views.Color, name="color" ),
       path('Howler/', views.Howler, name="howler"),
       path('specifications/', views.Patten, name="patten"),
       path('activate/', views.Activate, name="activate"),
       path('settings/', views.Settings, name="settings"),
       path('review/<str:slug>/', views.Review, name="review"),
       path('message/', views.Message_In, name="message"),
       path('content/<str:subject>/', views.Contented, name="contented"),
       path('cart/<str:slug>/', views.Mycart, name="cart"),
       path('wishlist/<str:slug>/', views.Mywishlist, name="wishlist"),
       path('viewcart/', views.Viewcart, name="viewcart"),
       path('viewwish/', views.Viewwish, name="viewwish"),
       path('cartdelete/<str:slug>/', views.Delcart, name="catdelte"),
       path('wishdelete/<str:slug>/', views.Delwish, name="wishdelte"),
       path('request/<str:slug>/', views.Request, name="request"),
       path('demand/', views.Demand, name="demand"),
       path('orders/', views.Orders, name="orders"),
       path('shop/<str:vessel>/', views.Shop, name="shop"),
       path('edit-store/<str:vessel>/', views.Amend, name="amend"),
       path('silver/', views.Silver, name="silver"),
       path('platinum/', views.Platinum, name="platinum"),
       path('titanium/', views.Titanium, name="titanium"),
       path('wallet/', views.Wallet, name="wallet"),
       path('withdraw/', views.Withdraw, name="withdraw"),
       path('silverMin/', views.Silver_Min, name="silvermin"),
       path('silverPro/', views.Silver_Pro, name="silverpro"),
       path('platinumMin/', views.Platinum_Min, name="platinumin"),
       path('platinumPro/', views.Platinum_Pro, name="platinumpro"),
       path('titaniumMin/', views.Titanium_Min, name="titaniummin"),
       path('titaniumPro/', views.Titanium_Pro, name="titaniumpro"),
       path('titaniumEnter/', views.Titanium_Enter, name="titaniumenter"),
       path('professinal/', views.Professinal, name="professinal"),
       path('erise-test/<str:vessel>/', views.Erise_text, name="erisetext"),
       path('contacts/', views.Contact_In, name="contact"),
       path('erise-contact/<str:vessel>/', views.Contact_Out, name="erisecontact"),
       path('create-contact/<str:vessel>/', views.Contact_Set, name="createcontact"),
       path('squeezes/', views.Listing, name="squeeze"),
       path('loan/', views.Loan, name="loan"),
       path('deletorder/<str:vessel>/', views.Order_Delete, name="orderdelete"),
       path('requestdelete/<str:vessel>/', views.Demand_Delete, name="requestdelete"),
       path('vieworder/<str:vessel>/', views.Vieworder, name="vieworder"),
       path('demandaccept/<str:vessel>/', views.Demand_Accepted, name="demandaccept"),
       path('shipping/<str:vessel>/', views.Shipping, name="shipping"),
       path('removeshiping/<str:vessel>/', views.Shipping_Remove, name="removeshiping"),
       path('orderprocess/', views.Orderprocess, name="orderprocess"),
       path('loancreate/', views.Loan_create, name="loancreate"),
       path('loanbase/<str:vessel>/', views.Loanbase, name="loanbase"),
       path('media/', views.Movies, name="moviesin"),
       path('moviescontent/', views.Movie_View, name="movielist"),
       path('moviedetails/<str:vessel>/', views.Movies_Details, name="moviedetail"),
       path('moviessoftwaregames/', views.Movies_Software_Games, name="mogasa"), 
       path('mainsetting/', views.Mainsetting, name="mainsetting"),
       path('search/', views.Search_View),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
