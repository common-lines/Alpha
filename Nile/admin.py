from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Client, Prime, Invoice, Stipulate, Vacate, Product, Store, Substitute, Lending, Movie, Center, Explore, Promotion, Search, Post
# Register your models here.
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'duration', 'verified','professional', 'institute')

class PrimeAdmin(admin.ModelAdmin):
    list_display = ('user','value','credit','extract','mine')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user','spender','code','value','remain','used')

class StipulateAdmin(admin.ModelAdmin):
    list_display = ('product','terminate','accepted','shipping','admin','payment','charge','reference')

#Views
admin.site.register(Client, ClientAdmin)
admin.site.register(Prime,PrimeAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Stipulate, StipulateAdmin)
admin.site.register(Vacate)
admin.site.register(Product,ProductAdmin)
admin.site.register(Store)
admin.site.register(Post)
admin.site.register(Substitute)
admin.site.register(Lending)
admin.site.register(Movie)
admin.site.register(Center)
admin.site.register(Explore)
admin.site.register(Promotion)
admin.site.register(Search)