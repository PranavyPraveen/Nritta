from django.urls import path

# from .views import home
from Homeapp import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register', views.register_fn, name='reg'),
    path('login', views.login_function, name='login'),
    path('logout', views.Logout_function, name='logout'),
    path('forgot', views.forgot_password, name="ft"),
    path('change/<str:p>/', views.change_password, name="cp"),
    path('tutorial/<int:i>/', views.tutorial_fn, name="tt"),
    path('video/<int:vdo>/', views.watch_fn, name="wt"),
    path('buycourse/<int:d>/', views.buy_course, name="bc"),
    path('subscribe', views.subscription, name='sn'),
    path('calculate-total/', views.calculate_total, name='calculate_total'),
    path('details', views.payment_pg, name='pt'),
    path('pay', views.final_amount, name='fp'),
    path('cd_select',views.card_select,name='cs'),
    path('user',views.login_dynamic, name='ld'),
    path('video-completed/', views.video_completed, name='video_completed'),
    path('cpdf/<int:id>/',views.generate_certificate,name='cpdf'),

]
