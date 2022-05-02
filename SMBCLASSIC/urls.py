"""SMBCLASSIC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',include("Frontview.urls" , namespace='frontview')),
    path('admin/', admin.site.urls),
    path('logistics/',include("Logistics.urls" , namespace='logistics')),
    path('user/',include("User.urls" , namespace='user')),
    path('branch/',include("Branch.urls", namespace='branch')),
    path('product/',include("Product.urls",namespace='product')),
    path('stock/',include("Stock.urls",namespace='stock')),
    path('preorder/',include("Pre_Order.urls",namespace='preOrder')),
    path('sales/',include("Sales.urls",namespace='sales')),
    path('credits/',include("Credit_Sales.urls",namespace='credit_sales')),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="user/passwordreset.html"),name='password_reset',),
    path('password_reset_done/',auth_views.PasswordResetView.as_view(template_name="user/password_reset_done.html"),name="password_reset_done",),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name='password_reset_confirm',),
    path( 'password_reset_completed/',auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name='password_reset_complete',),
]

urlpatterns+=staticfiles_urlpatterns()

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'errortemplate.views.page_not_found'
handler403 = 'errortemplate.views.permission_denied'
handler400 = 'errortemplate.views.bad_request'
