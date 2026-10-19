from django.urls import path
from . import views

urlpatterns=[path("events/",views.events,name="events"),
             path("events/<int:event_id>/",views.eventdetails,name="event_details"),
             path("events/addtocart/",views.addtocart,name="add_to_cart"),
             path("events/createevent/",views.Addevent,name="createevent"),
             path("cart/",views.Cart,name="cart")]