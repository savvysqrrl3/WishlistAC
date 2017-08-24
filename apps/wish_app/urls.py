from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^dashboard$', views.dashboard),
	url(r'^wish_items$', views.wish_items),
	url(r'^wish_items/create$', views.createItem),
	url(r'^show/(?P<id>\d+)$', views.show),
	url(r'^delete/(?P<id>\d+)$', views.deleteItem),
	url(r'^addItem/(?P<id>\d+)$', views.addItem),
	url(r'^removeItem/(?P<id>\d+)$', views.removeItem),
]