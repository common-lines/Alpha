from .models import Stipulate

def reque_demand(request): 

    if request.user.is_authenticated:
        user = request.user
        post_count_request = Stipulate.objects.filter(seller = user, terminate = False, admin = False, payment = False ).count() #order_by('-pk')
        post_data_request = Stipulate.objects.filter(seller = user, terminate = False, admin = False, payment = False ).order_by('-pk')[:10]
    else:
        post_count_request = 0
        post_data_request = None

    
    context={
        'post_count_request' : post_count_request,
        'post_data_request' : post_data_request,
    }
    return context