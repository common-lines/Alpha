from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.dispatch import receiver
from PIL import Image
from django.core.validators import URLValidator
from django.utils.timezone import now
from django.db.models import Sum, F, FloatField

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avater = models.ImageField(default='avater.jpg', upload_to='profile/', null=True)
    about = models.TextField(default="@Please Update Your Profile To Access Market",  null=True)
    phone = models.CharField(max_length=255, default="UNKNOWN", editable=True, null=True)
    subscription = models.CharField(default="Titanium", max_length=255, null=True)
    duration = models.IntegerField(default=15, null=True)
    terminate = models.DateField(auto_now=False, auto_now_add=False, default=now, blank=True )
    entirety = models.IntegerField(default=0, null=True)
    verified = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)
    software = models.BooleanField(default=False)
    ended = models.DateField(auto_now=False, auto_now_add=False, default=now, blank=True)
    institute = models.CharField(max_length=255, default="UNKNOWN", editable=True, null=True)
    region = models.CharField(max_length=255, default="UNKNOWN",  editable=True, null=True)
    country = models.CharField(max_length=255, default="UNKNOWN", editable=True, null=True) 

    def __str__(self):
        return str(self.user)
        #return self.user.username + "Client" DecimalField(decimal_places=2)
        #return f"{self.user.username} Client"
    def save(self, force_insert = False, force_update = False, using = None):
        super().save()

        img = Image.open(self.avater.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avater.path)
        

class Product(models.Model):
    title = models.CharField(max_length=255, editable=True, null=True) 
    price = models.FloatField()
    price_cancel = models.FloatField()
    sample = models.CharField(max_length=450, editable=True, null=True) 
    description = models.TextField()
    category = models.CharField(max_length=255, editable=True, null=True) 
    kind = models.CharField(max_length=25, editable=True, null=True) 
    availability = models.CharField(max_length=55, editable=True, null=True) 
    image = models.ImageField(default='avater.jpg', upload_to='product/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    country = models.BooleanField(default=False)
    zone = models.BooleanField(default=False)
    institute = models.BooleanField(default=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, editable=True, null=True) 
    terminate = models.DateField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.slug
   
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

class vision(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    image1 = models.ImageField(default='product.jpg', upload_to='product/', blank=True, null=True)
    image2 = models.ImageField(default='product.jpg', upload_to='product/', blank=True, null=True)
    image3 = models.ImageField(default='product.jpg', upload_to='product/', blank=True, null=True)
    image4 = models.ImageField(default='product.jpg', upload_to='product/', blank=True, null=True)
    image5 = models.ImageField(default='product.jpg', upload_to='product/', blank=True, null=True)
   
    def __str__(self):
        return str(self.product)
    

class size(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="None", editable=True, null=True, blank=True) 
    fild1 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    fild2 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    fild3 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    fild4 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    fild4 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
   
    def __str__(self):
        return str(self.product)

class color(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="None", editable=True, null=True, blank=True) 
    color1 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    color2 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    color3 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
    color4 = models.CharField(max_length=25, default="None",  editable=True, null=True, blank=True) 
    color4 = models.CharField(max_length=25, default="None", editable=True, null=True, blank=True) 
   
    def __str__(self):
        return str(self.product)

class pattern(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    tab1 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    tab2 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    tab3 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    tab4 = models.CharField(max_length=25, default="Not Found",  editable=True, null=True, blank=True) 
    tab5 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    det1 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    det2 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    det3 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True) 
    det4 = models.CharField(max_length=25, default="Not Found",  editable=True, null=True, blank=True) 
    det5 = models.CharField(max_length=25, default="Not Found", editable=True, null=True, blank=True)

    def __str__(self):
        return str(self.product)




class review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, default="Not Found", editable=True, null=True, blank=True)
    rating  = models.PositiveIntegerField(default=1)
    time = models.DateField(auto_now_add=True, null=True)
 

class Post(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='post_receiver', db_column='receiver')
    vendor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='post_sender', db_column='sender')
    title = models.CharField(max_length=255, default="Chat With Robot", editable=True, null=True, blank=True)
    slug = models.SlugField(unique=True, default="Chat-With-Robot")

    def __str__(self):
        return str(self.slug)



class Message(models.Model):
    subject = models.ForeignKey(Post, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='message_receiver', db_column='receiver')
    vendor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='message_sender', db_column='vendor')
    texting = models.TextField(default="Chat With Robot")
  
    def __str__(self):
        return str(self.subject)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)



class Stipulate(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='stipulate_seller', db_column='seller')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    marked = models.CharField(max_length=250, default="None", unique=True)
    terminate = models.BooleanField(default=False)
    size = models.CharField(max_length=250, default="None", editable=True, null=True, blank=True) 
    size01 = models.CharField(max_length=250, default="None", editable=True, null=True, blank=True)
    color = models.CharField(max_length=250, default="None", editable=True, null=True, blank=True) 
    color01 = models.CharField(max_length=250, default="None", editable=True, null=True, blank=True)
    extent  = models.PositiveIntegerField(default=1)
    accepted = models.BooleanField(default=False)
    shipping = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    charge = models.FloatField(default=0)
    reference = models.CharField(max_length=250, default="None")
    slot = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.marked)

    @property
    def get_total(self):
        total = self.product.price * self.extent
        return total

    @property
    def get_total_items(self):
        total = self.__class__.objects.all().aggregate(sum_all=Sum('extent')).get('sum_all')
        return total

    @property
    def get_total_price(self):
        total = self.__class__.objects.all().aggregate(total_price=sum(F('extent') * F('product__price'), output_field=FloatField() )).get('total_price')
        return total

    

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banner = models.ImageField(default='banner.jpg', upload_to='banners/', null=True)
    active = models.CharField(max_length=255, default="market", editable=True, null=True) 
    slogan = models.CharField(max_length=255, default="@Expore Beyond Limits.", editable=True, null=True) 
    twitter = models.URLField(default="https://twitter.com/Voxmart1", max_length=2000, validators=[URLValidator()])
    facebook = models.URLField(default="https://web.facebook.com/Voxmart-389747268420301", max_length=2000, validators=[URLValidator()])
    instagram = models.URLField(default="https://www.instagram.com/voxmart/", max_length=2000, validators=[URLValidator()])
    behance = models.URLField(default="https://www.linkedin.com/in/voxmart-online-396509186/", max_length=2000, validators=[URLValidator()])
    
    def __str__(self):
        return str(self.user)


class Prime(models.Model): #Wallet Table
    user = models.OneToOneField(User, on_delete=models.CASCADE) #user
    value = models.PositiveIntegerField(default=0) #amount available
    credit = models.PositiveIntegerField(default=0) # Last Withdwaw for payment
    extract = models.PositiveIntegerField(default=0) #Last payment with wallet withdwaw
    mine =  models.PositiveIntegerField(default=0) #last deposit receiveis

    def __str__(self):
        return str(self.user)

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='invouce_spender', db_column='spender')
    code = models.CharField(max_length=250, default="None", editable=True, null=True, blank=True) 
    phone = models.CharField(max_length=255, default="00-000-000-000", editable=True, null=True)
    value = models.PositiveIntegerField(default=0) #amount current value available
    remain = models.PositiveIntegerField(default=0) #amount Remain afetr payment
    holder = models.PositiveIntegerField(default=0) #amount sent to user wallet
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.code)

class Vacate(models.Model):#withdard dable
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount =  models.PositiveIntegerField(default=0) #amount current value available
    via =  models.CharField(max_length=255, default="None", editable=True, null=True)
    account =  models.CharField(max_length=255, default="+255-0700-000-000", editable=True, null=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='phone_user', db_column='phone')

    def __str__(self):
        return str(self.user)

class Substitute(models.Model):
    stipulate = models.OneToOneField(Stipulate, on_delete=models.CASCADE)
    seller = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.stipulate)



class Lending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Leander Name", editable=True, null=True, blank=True)
    slug = models.SlugField(unique=True, default="Chat-With-Robot")
    minmun = models.PositiveIntegerField(default=0)
    maxmum = models.PositiveIntegerField(default=0)
    collateral = models.CharField(max_length=25, default="None", editable=True, null=False, blank=False)
    duration = models.CharField(max_length=8, default="None", editable=True, null=False, blank=False)
    monthly = models.CharField(max_length=4, default="None", editable=True, null=False, blank=False)
    weeksii = models.CharField(max_length=4, default="None", editable=True, null=False, blank=False)
    weeklyr = models.CharField(max_length=4, default="None", editable=True, null=False, blank=False)
    loaninfo = models.TextField(default="None", editable=True, null=False, blank=False)
    collatexpl = models.TextField(default="None", editable=True, null=False, blank=False)
    loanrepay = models.TextField(default="None", editable=True, null=False, blank=False)
    wereap = models.TextField(default="None", editable=True, null=False, blank=False)
    location = models.CharField(max_length=255, default="None", editable=True, null=True) 
    terminate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    document = models.FileField(default='loan/documents/main.txt', upload_to='loan/documents/', blank=True, null=True)
    image = models.ImageField(default='product.jpg', upload_to='loan/', null=True)
    image2 = models.ImageField(default='product.jpg', upload_to='loan/', null=True)
    image3 = models.ImageField(default='product.jpg', upload_to='loan/', null=True)
    
    def __str__(self):
        return str(self.slug)
 
    def save(self, force_insert = False, force_update = False, using = None):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)
      

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title =  models.CharField(max_length=255, default="None", editable=True, null=True)
    slug = models.SlugField(unique=True, default="Chat-With-Robot")
    forename =  models.CharField(max_length=255, default="None", editable=True, null=True)
    price =  models.PositiveIntegerField(default=0)
    image = models.ImageField(default='product.jpg', upload_to='Movies/', null=True)
    requrement = models.TextField(default="None", editable=True, null=False, blank=False)
    location = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    terminate = models.DateField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return str(self.slug)


class Center(models.Model):
    title = models.CharField(max_length=255, default="None", editable=True, null=True)
    slug = models.SlugField(unique=True, default="voxmart-center-main")
    poster = models.CharField(max_length=255, default="P.O.Box", editable=True, null=True)
    phone = models.CharField(max_length=255, default="+255-700-000-000", editable=True, null=True)
    phone2 = models.CharField(max_length=255, default="+255-700-000-000", editable=True, null=True)
    email = models.EmailField(max_length=255, default="Voxmart@centers.admin", editable=True, null=True)
    email2 = models.EmailField(max_length=255, default="Voxmart@centers.admin", editable=True, null=True)
    oppening = models.CharField(max_length=255, default="08:00 a.m - 05:30 p.m", editable=True, null=True)
    weekend = models.CharField(max_length=255, default="09:30 a.m - 03:30 p.m", editable=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)

    def __str__(self):
        return str(self.slug)

class Explore(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    emplacement = models.CharField(max_length=255, default="Voxmart", editable=True, null=False, blank=False)

    def __str__(self):
        return str(self.center)


class Promotion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword2 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword3 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword4 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword5 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword6 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword7 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword8 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    keyword9 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category2 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category3 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category4 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category5 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category6 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    category7 = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    country = models.PositiveIntegerField(default=0)
    zone = models.PositiveIntegerField(default=0)
    institute = models.PositiveIntegerField(default=0)
    minmum = models.FloatField(default=5000.0)
    maxmum = models.FloatField(default=0)
    average = models.FloatField(default=0)
    terminate = models.DateField(auto_now=False, auto_now_add=False, default=now, blank=True )

    def __str__(self):
        return str(self.user)

class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    location = models.CharField(max_length=255, default="None", editable=True, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.location)
        


    







    

