from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from Alpha.utils import unique_slug
from .models import (
    Client, vision, size, color,
    pattern, Product, Post, Store,
    Prime, Stipulate, Substitute, Lending,
    Movie, Promotion
    )


#user Sugnal start
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.client.save()

#user Promation page
@receiver(post_save, sender=User)
def create_promotion(sender, instance, created, **kwargs):
    if created:
        Promotion.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_promotion(sender, instance, created, **kwargs):
    instance.promotion.save()

#create user store
@receiver(post_save, sender=User)
def create_store(sender, instance, created, **kwargs):
    if created:
        Store.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_store(sender, instance, created, **kwargs):
    instance.store.save()

#create user wallet
@receiver(post_save, sender=User)
def create_prime(sender, instance, created, **kwargs):
    if created:
        Prime.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_prime(sender, instance, created, **kwargs):
    instance.prime.save()

#user Sugnal ends 


#product Signals
#slug
@receiver(post_save, sender=Product)
def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug(instance, instance.title, instance)

pre_save.connect(slug_save, sender=Product)


@receiver(post_save, sender=Post)
def slug_save_post(sender, instance, *args, **kwargs):
    if instance.slug:
        instance.slug = unique_slug(instance, instance.title, instance)

pre_save.connect(slug_save_post, sender=Post)  


@receiver(post_save, sender=Lending)
def slug_save_lending(sender, instance, *args, **kwargs):
    if instance.slug:
        instance.slug = unique_slug(instance, instance.title, instance)

pre_save.connect(slug_save_post, sender=Lending)   


@receiver(post_save, sender=Movie)
def slug_save_movie(sender, instance, *args, **kwargs):
    if instance.slug:
        instance.slug = unique_slug(instance, instance.title, instance)

pre_save.connect(slug_save_post, sender=Movie)  



#slug
#vision Signals
@receiver(post_save, sender=Product)
def create_vision(sender, instance, created, **kwargs):

    if created:
        vision.objects.create(product=instance)

@receiver(post_save, sender=Product)
def save_vission(sender, instance, created, **kwargs):
    instance.vision.save()
#vision ends

#size signals
@receiver(post_save, sender=Product)
def create_size(sender, instance, created, **kwargs):

    if created:
        size.objects.create(product=instance)

@receiver(post_save, sender=Product)
def save_size(sender, instance, created, **kwargs):
    instance.size.save()
#size ends
#colors signals
@receiver(post_save, sender=Product)
def create_color(sender, instance, created, **kwargs):

    if created:
        color.objects.create(product=instance)

@receiver(post_save, sender=Product)
def save_color(sender, instance, created, **kwargs):
    instance.color.save()
#colors ends
#specification pattern
@receiver(post_save, sender=Product)
def create_pattern(sender, instance, created, **kwargs):

    if created:
        pattern.objects.create(product=instance)

@receiver(post_save, sender=Product)
def save_pattern(sender, instance, created, **kwargs):
    instance.pattern.save()

#specification pattern Ends

@receiver(post_save, sender=Stipulate)
def create_substitute(sender, instance, created, **kwargs):
    if created:
        Substitute.objects.create(stipulate=instance)

@receiver(post_save, sender=Stipulate)
def save_substitute(sender, instance, created, **kwargs):
    instance.substitute.save()


#product Signals ENDS
  



