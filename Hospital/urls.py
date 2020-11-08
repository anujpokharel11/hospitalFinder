from django.urls import path
from . import views
from django.views.generic import \
    TemplateView  # Need to import inorder to load the template directly without using the help of views.py

from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),

    # To Load Template directly without using views.py (This is important when you have to load the static template page)
    path('about/', TemplateView.as_view(template_name='Hospital/about.html'), name="about"),
    path('services/', TemplateView.as_view(template_name='Hospital/services.html'), name="services"),
    path('contact/', TemplateView.as_view(template_name='Hospital/contact.html'), name="contact"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.clientregisterPage, name="register"),
    path('clienthome/', views.clienthome, name="clienthome"),
    path('adminhome/', views.adminhome, name="adminhome"),
    path('customerdetail/', views.customerdetail, name="customerdetail"),
    path('detail/<int:hospital_id>/', views.detail, name='detail'),

    path('logoutall/', views.logoutall, name="logoutall"),

    # 1st step - Password reset garna ko lagi, email id halnu parxa so tyo page ko URL ho
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="Hospital/password_reset.html"),
         name="reset_password"),
    # auth_views.PasswordResetView.as_view  -> yaha  .as_view kina gareko vanda PasswordResetView chai django ko default class view ho so testo view ko lagi  .as_view garna parxa  &  testo defualt django view le default django template nai render garauxa.. so yedi hamilai django ko default template man parena vani teslai override pani garna sakxau . So, to override that page ->  (template_name="accounts/password_reset.html)

    # 2nd step - Email ID hali sake paxi, paswword reset link send vai sakyo tapaiko mail ma vanera jun page display hunxa tyo page ko lagi URL ho 
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="Hospital/password_reset_sent.html"),
         name="password_reset_done"),

    # 3rd Step - Naya Password halna ko lagi or Confirm garna ko lagi... yo page display garne URL ho
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="Hospital/password_reset_form.html"),
         name="password_reset_confirm"),
    # 4th Step - Password reset Sucess vai sake paxi,, password reset complete vayo aba tapai feri login garna saknu hunxa vanera jun Page display hunxa tesko URL ko lagi
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="Hospital/password_reset_done.html"),
         name="password_reset_complete"),

    path('hospital_list/', views.findHospital, name="hospital_list"),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
