from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard_hou', views.dashboard_house, name='dashboard_house'),
    path('dashboard_fav', views.dashboard_fav, name='dashboard_fav'),
    path('agent_dashboard_cus', views.agent_dashboard_cus, name='agent_customer'),
    path('agent_dashboard_bla', views.agent_dashboard_bla, name='agent_blacklist'),
    path('agent_dashboard_hou', views.agent_dashboard_hou, name='agent_house'),
    path('admin_dashboard_age', views.admin_dashboard_age, name='admin_agent'),
    path('admin_dashboard_bla', views.admin_dashboard_bla, name='admin_blacklist'),
    path('admin_dashboard_mvp', views.admin_dashboard_mvp, name='admin_mvp'),
    path('admin_dashboard_cus', views.admin_dashboard_cus, name='admin_customer'),
    path('fav_delete',views.fav_delete,name='fav_delete'),
    path('agent_add_blacklist',views.agent_add_blacklist,name='agent_add_blacklist'),
    path('agent_recover_bla', views.agent_recover_bla, name='agent_recover_bla'),
    path('agent_delete_hou_new', views.agent_delete_hou_new, name='agent_delete_hou_new'),
    path('agent_delete_hou_old', views.agent_delete_hou_old, name='agent_delete_hou_old'),
    path('admin_add_bla_cus', views.admin_add_blacklist_cus, name='admin_add_bla_cus'),
    path('admin_add_bla_age', views.admin_add_blacklist_age, name='admin_add_bla_age'),
    path('admin_recover_bla', views.admin_recover_bla, name='admin_recover_bla'),
    path('admin_add_mvp', views.admin_add_mvp, name='admin_add_mvp'),
    path('admin_delete_mvp', views.admin_delete_mvp, name='admin_delete_mvp'),

]
