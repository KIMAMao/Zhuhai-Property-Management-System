from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices, state_choices, statue_choices

from listings.models import Listing, Listing_old, Listing_new, sub_div
from realtors.models import Realtor

def index(request):
    # listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    listings = sub_div.objects.order_by('-price')[:3]
    # use sql and connection, no ORM
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings_sub_div ORDER BY price DESC LIMIT 3")
        listings = cursor.fetchall()

    listings = [sub_div(*row) for row in listings]


    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'statue_choices': statue_choices
    }

    return render(request, 'pages/index.html', context)


def about(request):
    # Get all realtors
    # realtors = Realtor.objects.order_by('-hire_date')
    # change to sql and conncection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM realtors_realtor ORDER BY hire_date DESC")
        realtors = cursor.fetchall()

    realtors = [Realtor(*row) for row in realtors]

    # Get MVP
    # mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    # change to sql and conncection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM realtors_realtor WHERE is_mvp = 1")
        mvp_realtors = cursor.fetchall()

    mvp_realtors = [Realtor(*row) for row in mvp_realtors]

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)


