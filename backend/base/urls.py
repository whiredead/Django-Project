from django.urls import path
from . import views
urlpatterns = [
    path('', views.HOME.as_view(), name='acceuil'),
    path('search_product', views.Search.as_view(), name='search'),
    path('product_by_cat/<int:args>', views.product_by_cat.as_view(), name='product_by_cat'),
    path('detail_product/<int:args>', views.detail_product.as_view(), name='detail'),
    path('signup', views.signUp, name='signup'),
    path('login', views.LOGIN, name='login'),
    path('logout', views.LOGOUT.as_view(), name='logout'),
    path('add_productcart/<int:args>', views.addtocart.as_view(), name='add_productcart'),
    path('mycart', views.cartdetail.as_view(), name='mycart'),
    path('emptycart', views.emptycart.as_view(), name='emptycart'),
    path('add/<int:args>', views.AddSameProduct.as_view(), name='add'),
    path('drop/<int:args>', views.DropProductInCart.as_view(), name='drop'),
    path('dropall/<int:args>',views.DropAll.as_view(), name='dropall'),
    path('address',views.CreateAddress, name='address'),
    path('complete',views.Complete,name='complete'),
    path('filter/<int:args>', views.Filter.as_view(), name='filter'),
    path('detailorder/<int:args>', views.detailorder.as_view(), name='detailorder'),
    path('myorders', views.orders.as_view(), name='myorders'),
    path('emailpassword', views.emailpassword, name='emailpassword'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('new_password', views.new_password, name='new_password'),

]