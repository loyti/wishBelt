from django.conf.urls import url
from . import views

urlpatterns = [
    #Home Page
    url(r'^$', views.index),
    url(r'^main$', views.index),

    #Wish List Page
    url(r'^dashboard$', views.itemsList),
    url(r'^addWish/(?P<item_id>\d+)$', views.addWish),
    url(r'^unWish/(?P<item_id>\d+)$', views.unWish),

    #Wish Item Page
    url(r'^item/(?P<item_id>\d+)$', views.itemInfo),

    #Processes
    url(r'^login$', views.signin),
    url(r'^register$', views.create_user),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^new_item$', views.new_item),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
]
