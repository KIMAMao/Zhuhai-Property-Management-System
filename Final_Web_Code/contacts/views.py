from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact, Contact_new, Fav


def contact(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        subdivision = request.POST['subdivision']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact_new.objects.all().filter(house_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/listing_old/' + listing_id)

        contact = Contact_new(house_id=listing_id, sub_id=subdivision, message=message, user_id=user_id)

        contact.save()

        # redirect to backpage
        return redirect('/listings/listing_old/' + listing_id)


def fav(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        user_id = request.POST['user_id']
        type = request.POST['type']
        listing_id_real = request.POST['listing_id_real']

    if type == '0':
    # Check if user has made inquiry already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Fav.objects.all().filter(sub_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already COLLECTED for this listing')
                return redirect('/listings/listing_div_old/' + listing_id_real)

        fav = Fav(user_id=user_id, sub_id=listing_id, type=type)

        fav.save()

        return redirect('/listings/listing_div_old/' + listing_id_real)

    if type == '1':
        # Check if user has made inquiry already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Fav.objects.all().filter(sub_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already COLLECTED for this listing')
                return redirect('/listings/listing_div/' + listing_id_real)

        fav = Fav(user_id=user_id, sub_id=listing_id, type=type)

        fav.save()

        return redirect('/listings/listing_div/' + listing_id_real)