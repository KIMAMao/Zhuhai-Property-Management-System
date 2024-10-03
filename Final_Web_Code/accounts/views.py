from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact_new
from realtors.models import Realtor
from contacts.models import Fav
from listings.models import Listing, Listing_new, Listing_old


# from listings.models import Listing


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        usertype = request.POST['user']

        # Check if passwords match
        if password == password2:
            #  Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'The email already exists')
                    return redirect('register')
                else:
                    # Everything passed
                    if usertype == '1':
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name, is_staff=True)
                        realtor = Realtor.objects.create(id=user.id, name=username,
                                                         email=email, is_mvp=0)
                        user.save()
                        realtor.save()
                    elif usertype == '2':
                        user = User.objects.create_superuser(username=username, password=password, email=email,
                                                             first_name=first_name, last_name=last_name)
                        user.save()
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name)
                        user.save()
                    messages.success(request, 'You are now registered and can Log In')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST['user']

        user = auth.authenticate(username=username, password=password)
        who = '0'
        if user is not None:
            if usertype == '2':
                if user.is_superuser:
                    who = '2'
            elif usertype == '1':
                if user.is_staff:
                    who = '1'

        if user is not None and usertype == who:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            if who == '1':
                return redirect('agent_customer')
            elif who == '2':
                return redirect('admin_customer')
            else:
                return redirect('dashboard_house')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')


def dashboard_house(request):
    house = Contact_new.objects.raw("""
    SELECT id, sub_id, house_id, message
    FROM contacts_contact_new
    WHERE user_id = %s
    ORDER BY id ASC
    """, [request.user.id])

    context = {
        'house': house,
    }

    return render(request, 'accounts/dash_house.html', context)


def dashboard_fav(request):
    love = Fav.objects.raw("""
    SELECT id, sub_id
    FROM contacts_fav
    WHERE user_id = %s
    ORDER BY id ASC
    """, [request.user.id])

    context = {
        'love': love
    }

    return render(request, 'accounts/dash_fav.html', context)


def agent_dashboard_cus(request):
    customer = User.objects.raw("""
    SELECT id, username, email
    FROM auth_user
    WHERE is_staff=0 and is_active=1
    ORDER BY id ASC 
    """)

    context = {
        'customer': customer,
    }

    return render(request, 'accounts/agent_customer.html', context)


def agent_dashboard_bla(request):
    blacklist = User.objects.raw("""
    SELECT id, first_name, last_name, username, email
    FROM auth_user
    WHERE is_active= 0 and is_staff= 0
    ORDER BY id ASC
    """)

    context = {
        'blacklist': blacklist,
    }

    return render(request, 'accounts/agent_blacklist.html', context)


def agent_dashboard_hou(request):
    houses_new = Listing_new.objects.raw("""
    SELECT id, room_num, area, price
    FROM listings_listing_new
    WHERE agent_id= %s
    ORDER BY id ASC
    """, [request.user.id])

    houses_old = Listing_old.objects.raw("""
        SELECT id, room_num, area, price
        FROM listings_listing_old
        WHERE agent_id= %s
        ORDER BY id ASC
        """, [request.user.id])

    context = {
        'house_new': houses_new,
        'house_old': houses_old
    }

    return render(request, 'accounts/agent_house.html', context)


def admin_dashboard_age(request):
    agent = User.objects.raw("""
    SELECT id, date_joined, last_login, email, username, first_name, last_name
    FROM auth_user
    WHERE is_staff=1 and is_superuser=0 and is_active=1
    ORDER BY id ASC 
    """)

    context = {
        'agent': agent,
    }

    return render(request, 'accounts/admin_agent.html', context)


def admin_dashboard_cus(request):
    customer = User.objects.raw("""
    SELECT id, date_joined, last_login, username, email
    FROM auth_user
    WHERE is_staff=0 and is_active=1
    ORDER BY id ASC 
    """)

    context = {
        'customer': customer,
    }

    return render(request, 'accounts/admin_customer.html', context)


def admin_dashboard_bla(request):
    blacklist = User.objects.raw("""
    SELECT id, first_name, last_name, username, email
    FROM auth_user
    WHERE is_active=0
    ORDER BY id ASC 
    """)

    context = {
        'blacklist': blacklist,
    }

    return render(request, 'accounts/admin_blacklist.html', context)


def admin_dashboard_mvp(request):
    mvp = Realtor.objects.raw("""
    SELECT id, description, name, email, hire_date, phone
    FROM realtors_realtor
    WHERE is_mvp=1
    ORDER BY id ASC 
    """)

    context = {
        'mvp': mvp
    }

    return render(request, 'accounts/admin_mvp.html', context)


def fav_delete(request):
    if request.method == "POST":
        defav_id = request.POST['fav_id']

    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM contacts_fav
        WHERE id = %s
        """, [defav_id])
    cursor.close()

    return redirect('dashboard_fav')


def agent_add_blacklist(request):
    if request.method == 'POST':
        black_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE auth_user
        SET is_active = 0
        WHERE id = %s
        """, [black_id])
    cursor.close()

    return redirect('agent_customer')


def agent_recover_bla(request):
    if request.method == 'POST':
        recover_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE auth_user
        SET is_active = 1
        WHERE id = %s
        """, [recover_id])
    cursor.close()

    return redirect('agent_blacklist')


def agent_delete_hou_new(request):
    if request.method == 'POST':
        house_id = request.POST['house_id']
    cursor = connection.cursor()
    cursor.execute("""
            DELETE FROM listings_listing_new
            WHERE id = %s
            """, [house_id])
    cursor.close()

    return redirect('agent_house')


def agent_delete_hou_old(request):
    if request.method == 'POST':
        house_id = request.POST['house_id']

    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM listings_listing_old
        WHERE id = %s
        """, [house_id])
    cursor.close()

    return redirect('agent_house')


def admin_add_blacklist_cus(request):
    if request.method == 'POST':
        black_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE auth_user
        SET is_active = 0
        WHERE id = %s
        """, [black_id])
    cursor.close()

    return redirect('admin_customer')


def admin_add_blacklist_age(request):
    if request.method == 'POST':
        black_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE auth_user
        SET is_active = 0
        WHERE id = %s
        """, [black_id])
    cursor.close()

    return redirect('admin_agent')


def admin_recover_bla(request):
    if request.method == 'POST':
        recover_id = request.POST['user_id']
    print(recover_id)

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE auth_user
        SET is_active = 1
        WHERE id = %s
        """, [recover_id])
    cursor.close()

    return redirect('admin_blacklist')


def admin_add_mvp(request):
    if request.method == 'POST':
        mvp_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE realtors_realtor
        SET is_mvp = 1
        WHERE id = %s
        """, [mvp_id])
    cursor.close()

    return redirect('admin_mvp')


def admin_delete_mvp(request):
    if request.method == 'POST':
        mvp_id = request.POST['user_id']

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE realtors_realtor
        SET is_mvp = 0
        WHERE id = %s
        """, [mvp_id])
    cursor.close()

    return redirect('admin_mvp')
