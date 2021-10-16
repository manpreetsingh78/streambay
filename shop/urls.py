from django.urls import path
from django.conf.urls import include, url
from .import views
# from polls.views import Home,success,failure

urlpatterns = [
    # url(r'^Success/',success),
    # url(r'^Failure/',failure),
    path('', views.home, name = "ShopHome"),
    path('home/', views.home, name = "ShopHome"),
    path('checkout/', views.checkout, name = "ShopCheckout"),
    path('contact/', views.contact, name = "ShopContact"),
    path('about/', views.about, name = "ShopAbout"),
    path('tracker/', views.tracker, name = "ShopTracker"),
    path('contact/', views.contact, name = "ShopContact"),
    path('replacement/', views.replacement, name = "ShopReplacement"),
    path('reset/', views.reset, name = "ShopReset"),
    # path('terms/', views.terms, name = 'ShopTerms'),
    # path('privacy/', views.privacy, name = 'ShopPrivacy'),
    # path('refund/', views.refund, name = 'ShopRefund'),
    # path('orderstatus/', views.handlerequest, name = "ShopHandleRequest"),
    # path('promo/', views.addcoupon, name = "ShopAddCoupon"),
    # path('payment_status', views.payment_status, name = 'payment_status'),
    # path('success/', views.success, name = "ShopHandleSuccess"),
    # path('failure/', views.failure, name = "ShopHandleFailure"),
]
