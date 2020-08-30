#Get Use Details
#
from django.utils.timezone import datetime, timedelta, timezone
from .models import Promotion
#

#Retrive Online Ads Specific For Every User

def interactive(request): 
    if request.user.is_authenticated:
        user = request.user
        
        #------------USER DATES AND TIME UPDATE
        #Update User Promotion Page Afret 90 days
        restore_date = request.user.promotion.terminate
        current_date_and_time = datetime.now()
        #Match User Date
        user_date = restore_date.strftime("%Y-%m-%d")
        current_date = current_date_and_time.strftime("%Y-%m-%d")
        #user Updater
        if current_date > user_date:
            existing = current_date_and_time + timedelta(days=91)
            main = existing.strftime("%Y-%m-%d")
            advertise = Promotion.objects.filter(user = request.user).update(
                keyword = "None", keyword2 = "None", keyword3 = "None",
                keyword4 = "None", keyword5 = "None", keyword6 = "None",
                keyword7 = "None", keyword8 = "None", keyword9 = "None",
                category = "None", category2 = "None", category3 = "None",
                category4 = "None", category5 = "None", category6 = "None",
                country =0, zone = 0, institute = 0, minmum = 5000.0,
                maxmum = 0.0, average = 0.0, terminate = main
                )           
        #------------//USER DATES AND TIME UPDATE//-----
        
        
    else:
        user = "Nothing Founded"

    context={
        'user_context' : user
    }
    return context