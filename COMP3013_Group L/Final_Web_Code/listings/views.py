from django.db import connection
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage
from .choices import price_choices, bedroom_choices, state_choices, statue_choices

from .models import Listing, sub_div, Listing_new, sub_div_old, Listing_old


def index(request):
    # listings choose the first 6 listings
    # listings = Listing_new.objects.order_by('-price')[:6]
    # use sql and connection to get the first 6 listings
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings_listing_new ORDER BY price DESC LIMIT 6")
        listings = cursor.fetchall()

    listings = [Listing_new(*row) for row in listings]

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing_new, pk=listing_id)

    # find the house_name in sub_div that div_id = s_num
    # div_name = get_object_or_404(sub_div, pk=listing.s_num)
    # name = div_name.house_name
    context = {
        'listing': listing,
        # 'div_name': name
    }

    return render(request, 'listings/listing.html', context)


def search(request):

    if 'statue' in request.GET:
        statue = request.GET['statue']
        if statue == '0':
            queryset_list = Listing_old.objects
        elif statue == '1':
            queryset_list = Listing_new.objects
    # queryset_list_2 = Listing_new.objects.order_by('-price')[:6]
    # # combine two querysets
    # queryset_list = list(queryset_list_1) + list(queryset_list_2)

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM listings_listing_new ORDER BY price DESC LIMIT 6")
    #     queryset_list = cursor.fetchall()

    # print(queryset_list)
    # queryset_list = [Listing_old(*listing_data) for listing_data in queryset_list]
    # queryset_list = [Listing_new(*listing_data) for listing_data in queryset_list]



    # KEYWORDS
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(room_num__icontains=keywords)
            # use sql
            # with connection.cursor() as cursor:
            #     cursor.execute("SELECT * FROM listings_listing_new WHERE listings_listing_new.room_num LIKE %s", ['%' + keywords + '%'])
            #     queryset_list = cursor.fetchall()
            #     queryset_list = [Listing_new(*listing_data) for listing_data in queryset_list]
    # # CITY
    # if 'city' in request.GET:
    #     city = request.GET['city']
    #     if city:
    #         queryset_list = queryset_list.filter(city__iexact=city)

    # STATE
    if 'state' in request.GET:
        state = request.GET['state']
        # if state:
            # queryset_list = queryset_list.filter(district__iexact=state)
            # district value from sub_div database, connected two databases by using div_id = s_num
            # queryset_list = queryset_list.filter(district__iexact=state)

            # with connection.cursor() as cursor:
            #     # execute the sql and DELETE the data in order to keep the original format
            #     cursor.execute("SELECT * "
            #                    "FROM listings_listing_new "
            #                    "JOIN listings_sub_div ON listings_listing_new.s_num = listings_sub_div.div_id "
            #                    "WHERE listings_sub_div.district LIKE %s"
            #                    ""
            #                    , ['%' + state + '%'])
            #
            #     queryset_list = cursor.fetchall()

    # PRICE
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
        'statue_choices': statue_choices
    }

    return render(request, 'listings/search.html', context)


def listing_div(request, listing_div_id):
    listing_div = get_object_or_404(sub_div, pk=listing_div_id)

    # use sql and connection to get
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM listings_sub_div")
    #     listing_div = cursor.fetchall()
    #
    # listing_div = [sub_div(*listing_data) for listing_data in listing_div]
    #
    # listing_div = [listing for listing in listing_div if listing.div_id == listing_div_id]
    context = {
        'listing_div': listing_div
    }

    return render(request, 'listings/listing_div.html', context)


def index_div(request):
    listings = sub_div.objects.order_by('-price')

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings_div.html', context)


def search_div(request, listing_div_id):
    # join sub_div ON sub_div.div_id = listing_new.s_num
    queryset_list = Listing_new.objects.raw('SELECT * '
                                            'FROM listings_listing_new '
                                            'JOIN listings_sub_div '
                                            'ON listings_listing_new.s_num = listings_sub_div.div_id '
                                            'WHERE listings_sub_div.div_id = %s', [listing_div_id])
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM listings_listing_new WHERE s_num=%s ORDER BY agent_id DESC",[listing_div_id])
    #     queryset_list = cursor.fetchall()

    # print(queryset_list)

    # queryset_list = [Listing_new(*listing_data) for listing_data in queryset_list]

    # print(queryset_list)
    # KEYWORDS
    # if 'keywords' in request.GET:
    #     keywords = request.GET['keywords']
    # if listing_div_id:
    #     queryset_list = queryset_list.filter(s_num__iexact=listing_div_id)
    # queryset_list = [listing for listing in queryset_list if listing.s_num == listing_div_id]
    # print("=============")
    # print(queryset_list)
    # print("=============")

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)


def index_div_old(request):
    # listings = sub_div_old.objects.order_by('district')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings_sub_div_old ORDER BY district")
        data = cursor.fetchall()

    data = [sub_div_old(*listing_data) for listing_data in data]

    paginator = Paginator(data, 9)
    num_p = request.GET.get('page', '1')
    try:
        page = paginator.page(num_p)
    except(PageNotAnInteger, EmptyPage, InvalidPage):
        page = paginator.page('1')

    if page.paginator.num_pages >= 13:
        ifEllipsis = 1
        range1 = range(1, 13)
        range2 = range(1, 15)
        range3 = range(1, 14)
        lastButOne = page.paginator.num_pages - 1
    else:
        ifEllipsis = 0

    context = {
        'page': page,
        'range1': range1,
        'range2': range2,
        'range3': range3,
        'ifEllipsis': ifEllipsis,
        'lastButOne': lastButOne
    }


    return render(request, 'listings/listings_div_old.html', context)


def listing_div_old(request, listing_div_id):
    listing_div_old = get_object_or_404(sub_div_old, pk=listing_div_id)
    # listing_div_old = sub_div_old.objects.raw('SELECT * FROM listings_sub_div_old WHERE div_id = %s', [listing_div_id])
    # in connection and sql, we need to use the table name
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM listings_sub_div_old WHERE div_id = %s", [listing_div_id])
    #     listing_div_old = cursor.fetchall()

    # listing_div_old = [sub_div_old(*listing_data) for listing_data in listing_div_old]

    context = {
        'listing': listing_div_old
    }

    return render(request, 'listings/listing_div_old.html', context)


def search_div_old(request, listing_div_id):
    # queryset_list = Listing_old.objects.order_by('-price').filter(s_num__iexact=listing_div_id)
    # use connection and sql to get the data
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings_listing_old WHERE s_num = %s", [listing_div_id])
        queryset_list = cursor.fetchall()

    queryset_list = [Listing_old(*listing_data) for listing_data in queryset_list]
    # KEYWORDS
    # if 'keywords' in request.GET:
    #     keywords = request.GET['keywords']

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search_div_old.html', context)


def listing_old(request, listing_id):
    listing = get_object_or_404(Listing_old, pk=listing_id)
    # use connection and sql to get the data
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM listings_listing_old WHERE id = %s", [listing_id])
    #     listing = cursor.fetchall()
    # find the house_name in sub_div that div_id = s_num

    # div_name = get_object_or_404(sub_div_old, pk=listing.s_num)

    # find the house_name in sub_div that div_id = s_num
    # div_name = get_object_or_404(sub_div, pk=listing.s_num)
    # name = div_name.house_name
    context = {
        'listing': listing,
    }

    return render(request, 'listings/listing_old.html', context)
