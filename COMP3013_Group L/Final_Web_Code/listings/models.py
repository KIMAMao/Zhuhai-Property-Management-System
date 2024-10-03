from django.db import models
from datetime import datetime
from realtors.models import Realtor

class sub_div_old(models.Model):
    # sub_url,photo,build_year,house_name,address,price,district,div_id,property_company,developer,property_fee,house_type,surr_envi,surr_school,surr_trafic,surr_business,surr_entertain
    sub_url = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    build_year = models.IntegerField()
    house_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    district = models.CharField(max_length=200)
    div_id = models.CharField(max_length=200)
    property_company = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    property_fee = models.CharField(max_length=200)
    house_type = models.CharField(max_length=200)
    surr_envi = models.CharField(max_length=200)
    surr_school = models.CharField(max_length=200, default='0')
    surr_trafic = models.CharField(max_length=200, default='0')
    surr_business = models.CharField(max_length=200, default='0')
    surr_entertain = models.CharField(max_length=200, default='0')


    def __str__(self):
        return self.house_name


class sub_div(models.Model):
    # sub_url,photo,house_name,house_status,house_type,address,price,district,developer,sur_trafic,sur_school,sur_environment,sur_business,sur_entertain,peoperty_fee,property_company
    sub_url = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    house_name = models.CharField(max_length=200)
    house_status = models.CharField(max_length=200)
    house_type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    div_id = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    sur_trafic = models.CharField(max_length=200)
    sur_school = models.CharField(max_length=200)
    sur_environment = models.CharField(max_length=200)
    sur_business = models.CharField(max_length=200)
    sur_entertain = models.CharField(max_length=200)
    peoperty_fee = models.CharField(max_length=200)
    property_company = models.CharField(max_length=200)

    def __str__(self):
        return self.house_name


class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class Listing_new(models.Model):
    # photo,room_num,area,price,orientation,h_num,s_num,agent_id
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    room_num = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    orientation = models.CharField(max_length=200)
    h_num = models.CharField(max_length=200)
    s_num = models.CharField(max_length=200)
    agent_id = models.IntegerField()

    def __str__(self):
        return self.h_num

class Listing_old(models.Model):
    # photo,room_num,area,price,status,h_num,s_num,orientation,agent_id
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    room_num = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=200)
    h_num = models.CharField(max_length=200)
    s_num = models.CharField(max_length=200)
    orientation = models.CharField(max_length=200)
    agent_id = models.IntegerField()


