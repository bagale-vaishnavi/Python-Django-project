# Import the necessary modules
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.products, name="products"),
    path("checkout/", views.checkout, name="checkout"),
    #path('payment-status/', views.payment_status, name='payment_status'),
    path("cart/", views.cart, name="cart"),
    #path("handlerequest/", views.handlerequest, name="handlerequest")
]

# Static file handling for development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  # Ensure this is only active during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler500 = 'myapp.views.custom_500'