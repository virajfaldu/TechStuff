from django.urls import path,include
from . import views

urlpatterns = [
	#Blog Post Related Urls
    path('', views.index, name="Home"),
    path('post/<str:title>/', views.show_post, name="show_post"),
    path('cate/<str:title>/', views.show_cate, name="show_cate"),
    path('add_like/', views.add_like, name='like'),
    path('remove_like/', views.remove_like, name='dis_like'),
    path('add_comment/', views.add_comment, name='comment'),
    path('add_post/', views.add_post, name='add_post'),
    path('approve/', views.post_approve, name='post_approve'),
    path('action/<str:act>/<int:pid>/', views.action, name='action_post'),
    path('search/', views.search, name="Search"),

    #User Related Urls
    path('logout/', views.auth_logout, name="Logout"),
    path('signin/',views.auth_register, name="Register"),
    path('login/', views.auth_login, name="Login"),
    path('contact/', views.contact, name='contact_us'),
    path('account/', views.user_account, name='user_account')
]

