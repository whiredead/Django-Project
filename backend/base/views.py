
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.db.models import Count
from datetime import datetime, timedelta
from django.http import HttpResponse
# Create your views here.

class HOME(View):
    def get(self,request):
        produit = Product.objects.all()
        return render(request, "HOME.html", {'produits':produit})


class Search(View):
    def get(self,request):
        """ retrieve searched producted by form GET """
        product_searched = request.GET["product_searched"]
        """ retrieve  0§ searched producted by description """
        produits_recherche = Product.objects.filter(description__icontains=product_searched)
        return render(request, "search_product.html", {'produit':produits_recherche, 'cle': product_searched})


class product_by_cat(View):
    def get(self,request,args):
        """ retrieve id category by args in url """
        cat = Category.objects.get(id=args)
        """ retrieve product by id category """
        produit_par_cat = Product.objects.filter(id_cat=args)
        return render(request, 'listproduct.html', {'produit':produit_par_cat, 'categorie':cat})


class Filter(View):
    def get(self, request, args):
        if args == 1:
            produit = Product.objects.order_by('name')

        elif args == 2:
            produit = Product.objects.order_by('price')
        else:
            produit = Product.objects.order_by('nbr_purchase')
        return render(request, "HOME.html", {'produits': produit})


class detail_product(View):
    """by image"""
    def get(self,request,args):
        """ retrieve product name by args in url """
        produits = Product.objects.get(pk=args)
        """ retrieve all pictures of this product """
        images = Pictures.objects.filter(id_prod=args)
        """ retrieve all products of same category """
        prodcat=Product.objects.filter(id_cat=produits.id_cat)
        """ send the product informations to detailproduct.html """
        return render(request,'detail.html',{'produits':produits, 'picture': images, 'prodcat':prodcat})


def signUp(request):
    if request.POST.get("btn"):
        usern = request.POST.get("username")
        password = request.POST.get("password")
        mail = request.POST.get("email")
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        # check if username already exist
        # retrieve customer in db with the same usernmane or email given in form and table customer table !=0
        check_existing_username = User.objects.filter(username=usern) and Customer
        check_existing_email = User.objects.filter(email=mail) and Customer
        check_existing_phone = Customer.objects.filter(phone=phone) and Customer
        if check_existing_username:
            message = "Username taken"
            return render(request, 'login.html', {'msg': message})
        elif check_existing_phone :
            message = "phone taken"
            return render(request, 'login.html', {'msg': message})
        elif check_existing_email:
            message = "email taken"
            return render(request, 'login.html', {'msg': message})
        else:
            #create the user
            user = User.objects.create_user(usern, mail, password)
            cust = Customer.objects.create(user=user, fullname=fullname, phone=phone)
            cart = Cart.objects.create(id_cust=cust, GlobalPrice=0)
            html = render_to_string('SignupEmail.html')
            request.session['mail'] = mail
            send_mail(
                'SingUp',
                'SignupEmail.html',
                'shopgamerfirst@gmail.com',
                [mail],
                html_message=html,
                fail_silently=False,
            )
            login(request, user)
            return redirect('address')
    else:
        return render(request, 'login.html', {})


def CreateAddress(request):
    #This method is called when valid form data has been posted.
    #retrieve the User information from the form posted.
    if request.POST.get('btnaddress'):
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")
        country = request.POST.get("country")
        if address_2 is not None:
            address = ShipmentAddress.objects.create(cust_id=request.user.customer.id, address_1=address_1, address_2=address_2,
                                                     zip_code=zip_code, city=city, country=country)
        else:
            address = ShipmentAddress.objects.create(cust_id=request.user.customer.id, address_1=address_1,
                                                     zip_code=zip_code, city=city, country=country)
        return redirect('acceuil')
    else:
        return render(request,'address.html',{})


def forgetpassword(request):
    return render(request,'resetpassword.html',{})


def emailpassword(request):
    mail = request.POST.get('email')
    check_existing = User.objects.filter(email=mail)
    if check_existing:
        html = render_to_string('PasswordEmail.html')
        request.session['mail'] = mail
        send_mail(
            'Reset Your Password',
            'PasswordEmail.html',
            'shopgamerfirst@gmail.com',
            [mail],
            html_message=html,
            fail_silently=False,
        )
        messages = 'check your mail inbox'
        return render(request, 'resetpassword.html', {'msg': messages})
    else:
        messages = 'there is no such user with this email'
        return render(request, 'resetpassword.html', {'msg': messages})


def new_password(request):
    return render(request,'new_password.html',{})


def reset_password(request):
    new_password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if new_password != confirm_password:
        messages='confirm password and Password does not match'
        return render(request,'new_password.html',{'msg':messages})
    else:
        mail = request.session.get('mail')
        user = User.objects.get(email=mail)
        user.set_password(new_password)
        user.save()
        print('user#########',user.password)
        return redirect('login')


def LOGIN(request):
    if request.POST.get("btn"):
        usern =request.POST.get("username")
        pswd =request.POST.get("password")
        user = authenticate(username=usern, password=pswd)
        if user is not None:
            login(request,user)
            return redirect('acceuil')
        else:
            message = "Username OR password incorrect"
            return render(request, 'login.html', {'msg': message})
    else:
        return render(request, 'login.html',{})


class LOGOUT(View):
    def get(self, request):
        logout(request)
        return redirect('acceuil')


class addtocart(View):
    def get(self,request,args):
        if request.user.is_authenticated:
            # retrieve product want to add to cart by his primary key sent in the url
            productAddToCart = Product.objects.get(pk=args)
            # retrieve the cart of customer
            cart = request.user.customer.cart.id
            cartSessionObj = Cart.objects.get(id=cart)
            # retrieve all product Cart
            productInCart = ProductCart.objects.filter(id_cart=cartSessionObj.pk,is_order=False)
            # check if productAddToCart exists in productInCart
            exist = 0
            for ele in productInCart:
                # methode ajout d'un produit existant
                if ele.id_prod.id == productAddToCart.id:
                    exist = 1
                    # check if I can buy certain quantity of a product
                    if productAddToCart.countInStock > ele.QuantityProd:
                        ele.QuantityProd = ele.QuantityProd + 1
                        ele.TotalPrice += productAddToCart.price
                        ele.save()
                        cartSessionObj.GlobalPrice = cartSessionObj.GlobalPrice + productAddToCart.price
                        cartSessionObj.save()
                        break
                    else:
                        messages.info(self.request, "impossible to perform this operation")
                        return redirect('acceuil')
                        break
            # methode ajout d'un produit non existant
            if exist == 0:
                ProductCart.objects.create(id_cart=cartSessionObj, id_prod=productAddToCart,
                                           QuantityProd=1, TotalPrice=productAddToCart.price)
                cartSessionObj.GlobalPrice = cartSessionObj.GlobalPrice + productAddToCart.price
                cartSessionObj.save()
            # return to the previous url (request.META.get('HTTP_REFERER'))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            message = "You Must Login OR Sign up First "
            return render(request, 'login.html', {'msg': message})


class cartdetail(View):
    def get(self,request):
        """retrieve the cart customer"""
        cartSessionObj = Cart.objects.get(id=request.user.customer.cart.id)
        productcart = ProductCart.objects.filter(id_cart=request.user.customer.cart.id, is_order=False)
        """retrieve the productcart of the cart session"""
        prix = cartSessionObj.GlobalPrice
        # convert = convert_money(Money(prix.amount,prix.currency), 'USD')
        convert = prix.amount / 10
        try:
            orders = Order.objects.filter(id_cust=request.user.customer)
        except:
            return render(request, 'Mycart.html', {'productofcart': productcart, 'Price': prix,
                                                   'idmycart': request.user.customer.cart.id, 'convert_price': convert})
        else:
            try:
                iter(orders)
            except TypeError:
                print("############ not iterable")
                iterable = 0
            else:
                iterable = 1
            return render(request, 'Mycart.html', {'productofcart': productcart, 'Price': prix,
                                                   'idmycart': request.user.customer.cart.id,
                                                   'convert_price': convert, 'orders': orders, 'iterable': iterable})


class emptycart(View):
    def get(self,request):
        try:
            orders = Order.objects.get(id_cust=request.user.customer)
        except:
            return render(request, 'emptycart.html',{})
        else:
            try:
                iter(orders)
            except TypeError:
                print("############ not iterable")
                iterable = 0
            else:
                iterable = 1
            print("###############", orders.id)
            return render(request, 'emptycart.html', {'orders': orders, 'iterable': iterable})


class AddSameProduct(View):
    def get(self,request,args):
        """retrieve the product want to add"""
        productWantadd=ProductCart.objects.get(id_prod=args,is_order=False)
        product = Product.objects.get(pk=productWantadd.id_prod.id)
        """retrieve the original price of product want to add"""
        prixoriginal = (productWantadd.TotalPrice / productWantadd.QuantityProd)
        """increment quantite and price of the current product in cart"""
        if product.countInStock > productWantadd.QuantityProd:
            productWantadd.QuantityProd += 1
            productWantadd.TotalPrice += prixoriginal
            productWantadd.save()
            """retrieve the cart of product want to add"""
            Currentcart = Cart.objects.get(pk=productWantadd.id_cart.pk)
            """increment globalPrice of the cart"""
            Currentcart.GlobalPrice += prixoriginal
            Currentcart.save()
            return redirect('mycart')
        else:
            messages.info(self.request, "impossible to perform this operation")
            return redirect('mycart')


class DropProductInCart(View):
    def get(self, request, args):
        """retrieve the productcart want to drop"""
        productWantdrop = ProductCart.objects.get(id_prod=args,is_order=False)
        """retrieve the cart of product want to drop"""
        Currentcart = Cart.objects.get(pk=productWantdrop.id_cart.pk)
        """decrease globalPrice of the cart"""
        Currentcart.GlobalPrice = Currentcart.GlobalPrice - productWantdrop.TotalPrice
        Currentcart.save()
        productWantdrop.delete()
        return redirect('mycart')


class DropAll(View):
    def get(self, request, args):
        """retrieve the cart want to drop"""
        carttodrop=Cart.objects.get(pk=args)
        """retrieve the product cart of the cart"""
        product_cart_to_drop=ProductCart.objects.filter(id_cart=args,is_order=False)
        for prod in product_cart_to_drop:
            prod.delete()
        carttodrop.GlobalPrice = 0
        carttodrop.save()
        return redirect('emptycart')


def Complete(request):
    print("########################### Complete ################")

    #createorder(request)
    print("########################### create order ################")

    #retrieve the price of the cart want to buy
    product = ProductCart.objects.filter(id_cart=request.user.customer.cart.id, is_order=False)
    total = Cart.objects.filter(id_cust=request.user.customer).values("GlobalPrice")
    address = ShipmentAddress.objects.get(cust=request.user.customer)
    #retrieve the product of the cart want to buy
    # create order
    order = Order.objects.create(id_cust=request.user.customer, TotalPrice=total[0]['GlobalPrice'])

    print("########################### fin create order ################")
    print("########################### send mail ################")
    context = {'order': order, 'produit': product, 'total': total[0]['GlobalPrice'],
               'address': address}
    html = render_to_string('email order.html', context)
    send_mail(
        'Purchase',
        'email order.html',
        'shopgamerfirst@gmail.com',
        [request.user.email],
        html_message=html,
        fail_silently=False,
    )
    print("########################### fin send mail ################")

    # product.QuantityProd
    """for pro in product:
        print('#################### product quantite ###',pro.QuantityProd)
        print('#################### product  price ###',pro.TotalPrice)
        print('#################### product total id_prod ###',pro.id_prod.name)

    if address.address_2:
        print('##################### address_2 ##',address.address_2)
    else:
        print("none")
    print('##################### total ##',total[0]['GlobalPrice'])"""

    """
    try:
        iter(orders)
    except TypeError:
        print("############ not iterable")
        ProdOrder = ProductOrder.objects.filter(id_order=orders.id)
        for pp in ProdOrder:
            print('################ product order###',pp.QuantityProd)
            prodDB = Product.objects.filter(id=pp.id_prod_id)
            print('################ product db ####',prodDB)

    else:
        print("############iterable")
        for order in orders:
            ProdOrder = ProductOrder.objects.filter(id_order=order.id)
            print('################ product order', ProdOrder)
            for Prod in ProdOrder:
                prodDB = Product.objects.filter(id=Prod.id_prod_id)
    """

    # buy_cart(request)

    print("########################### buy cart################")

    # retrieve the cart want to buy
    cart_to_buy = Cart.objects.get(pk=request.user.customer.cart.id)
    # retrieve the productcart of the cart
    # implementation de confirmation
    for prod_of_cart in product:
        # retrieve the specific product to change in db
        prodToChange = Product.objects.get(pk=prod_of_cart.id_prod.id)
        print("############## pro db before", prodToChange.countInStock)
        # change the object
        prodToChange.countInStock = prodToChange.countInStock - prod_of_cart.QuantityProd
        prodToChange.nbr_purchase += prod_of_cart.QuantityProd
        prodToChange.save()
        print("############## pro db after", prodToChange.countInStock)
    # emptycart
    cart_to_buy.GlobalPrice = 0
    cart_to_buy.save()
    print("########################### fin buy cart################")

    product.update(id_order=order)
    product.update(is_order=True)
    print("########################### fin Complete################")
    return redirect("acceuil")


class orders(View):
    def get(self,request):
        orders=Order.objects.filter(id_cust=request.user.customer)
        return render(request,'base.html',{"orders":orders})


class detailorder(View):
    def get(self,request,args):
        order = Order.objects.get(id=args)
        product = ProductCart.objects.filter(id_order=order)
        return render(request, 'orders.html', {'product': product, 'order': order})


"""
class AllOrders(View):
    def get(self,request):
        queryset = ProductCart.objects.none()
        orders = Order.objects.filter(id_cust=request.user.customer)
        for ord in orders:
            prod = ProductCart.objects.filter(id_order=ord)
            for ele in prod:
                queryset |= ProductCart.objects.filter(pk=ele.pk)
        print("#################",type(queryset),'############',queryset)
        return render(request, 'orders.html', {'orders': orders, 'productbuy': queryset})
"""


"""
class LOGIN(FormView):
    #the attributs of FormView
    template_name = 'firstlogin.html'
    #construire formulaire a l aide loginForm
    form_class = loginForm
    success_url = reverse_lazy("acceuil")

    def form_valid(self, form):
        #retrieve the User information from the form posted.
        name = form.cleaned_data.get("username")
        pswd = form.cleaned_data.get("password")
        #recherecher user if oui user=user else user=none
        user = authenticate(username=name, password=pswd)
        if user is not None:
            login(self.request, user)
        else:
            messages.info(self.request, "Username OR password incorrect")
            print(messages,"##########")
            "form is the form generate by form_class=loginForm"
            return render(self.request, 'firstlogin.html', {'message':messages,'form':form})
        return super().form_valid(form)

class signUp(CreateView):
    #the attributs of CreateView
    #the CreateView use for creating an object and generate a Form
    template_name = "FirstSignUp.html"
    form_class = signupForm
    success_url = reverse_lazy("acceuil")

    def form_valid(self, form):
        #This method is called when valid form data has been posted.
        #retrieve the User information from the form posted.
        usern = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        mail = form.cleaned_data.get("email")
        number = form.cleaned_data.get("phone")
        #check if username already exist
        #retrieve customer in db with the same usernmane or email given in form and table customer table !=0
        check_existing_username = User.objects.filter(username=usern) and Customer
        check_existing_email = User.objects.filter(email=mail) and Customer
        if check_existing_username:
            messages.info(self.request, "Username taken")
            return redirect('signup')
        elif check_existing_email:
            messages.info(self.request, "email taken")
            return redirect('signup')
        else:
            #create the user
            user = User.objects.create_user(usern, mail, password)
            form.instance.user = user
            login(self.request, user)
        return super().form_valid(form)

class addtocart(View):
    def get(self,request,args):
        if request.user.is_authenticated:
            print(request.user.customer,"#################")
            # retrieve product want to add to cart by his primary key sent in the url
            productAddToCart = Product.objects.get(pk=args)
            # check if cart exists if exist (cart_id=id) else (cart_id=None)
            cartId = self.request.session.get("cart_id", None)
            # cart exists
            if cartId:
                # retrieve Cart object of the session from db
                cartSessionObj = Cart.objects.get(id=cartId)
                # retrieve all product Cart
                productInCart = ProductCart.objects.filter(id_cart=cartSessionObj.pk)
                # check if productAddToCart exists in productInCart
                exist = 0
                for ele in productInCart:
                    # methode ajout d'un produit existant
                    if ele.id_prod.id == productAddToCart.id:
                        exist = 1
                        # check if i can buy certain quantity of a product
                        if productAddToCart.countInStock > ele.QuantityProd:
                            ele.QuantityProd = ele.QuantityProd + 1
                            ele.TotalPrice += productAddToCart.price
                            ele.save()
                            cartSessionObj.GlobalPrice = cartSessionObj.GlobalPrice + productAddToCart.price
                            cartSessionObj.save()
                            break
                        else:
                            messages.info(self.request, "impossible to perform this operation")
                            return redirect('acceuil')
                            break
                        # methode ajout d'un produit non existant
                if exist == 0:
                    ProductCart.objects.create(id_cart=cartSessionObj, id_prod=productAddToCart,
                                               QuantityProd=1, TotalPrice=productAddToCart.price)
                    cartSessionObj.GlobalPrice = cartSessionObj.GlobalPrice + productAddToCart.price
                    cartSessionObj.save()
            # cart not exists
            else:
                # create a cart
                cartSessionObj = Cart.objects.create(id_cust=request.user.customer, GlobalPrice=0)
                # modify the cart session id
                self.request.session['cart_id'] = cartSessionObj.id
                ProductCart.objects.create(id_cart=cartSessionObj, id_prod=productAddToCart,
                                           QuantityProd=1, TotalPrice=productAddToCart.price)
                cartSessionObj.GlobalPrice += productAddToCart.price
                cartSessionObj.save()
                # return to the previous url (request.META.get('HTTP_REFERER'))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(self.request, "You Must Login OR Sign up ")
            return redirect('login')
            
            
class cartdetail(View):
    def get(self,request):
        #retrieve the cart id of the session
        cartid = request.session.get('cart_id',None)
        if cartid is not None:
            #retrieve  cart 
            cart = Cart.objects.get(pk=cartid)
            #retrieve the productcart of the cart session
            productcart=ProductCart.objects.filter(id_cart=cartid)
            prix=cart.GlobalPrice
            return render(request,'Mycart.html',{'productofcart':productcart,'Price':prix,'idmycart': cartid})
        else:
            return redirect('emptycart')
            
            
class Confirm(View):
    def get(self, request, args):
        #retrieve the cart want to drop
        cart_to_buy = Cart.objects.get(pk=args)
        #retrieve the productcart of the cart
        product_cart_to_buy = ProductCart.objects.filter(id_cart=args)
        ruptureStock = 0
        for prodcart in product_cart_to_buy:
            if prodcart.QuantityProd > prodcart.id_prod.countInStock:
                ruptureStock = 1
                break

        if ruptureStock == 0: #check if not rupture
            #implementation de confirmation
            for prod_of_cart in product_cart_to_buy:
                #retrieve the specific product to change in db
                prodToChange=Product.objects.get(pk=prod_of_cart.id_prod.id)
                #change the object
                prodToChange.countInStock = prodToChange.countInStock - prod_of_cart.QuantityProd
                prodToChange.nbr_purchase += prod_of_cart.QuantityProd
                prodToChange.save()
            # rendre cart empty
            for prod_to_drop in product_cart_to_buy:
                prod_to_drop.delete()

            cart_to_buy.GlobalPrice = 0
            cart_to_buy.save()
            messages.info(self.request, "Thanks for your purchase see you again")
            return redirect('acceuil')
        else:
            messages.info(self.request, " One or more product is out of stock  ")
            return redirect('mycart')


class Confirm(View):
    def get(self, request, args):
        #retrieve the cart want to drop
        cart_to_buy = Cart.objects.get(pk=args)
        #retrieve the productcart of the cart
        product_cart_to_buy = ProductCart.objects.filter(id_cart=args)
        #implementation de confirmation
        for prod_of_cart in product_cart_to_buy:
            #retrieve the specific product to change in db
            prodToChange=Product.objects.get(pk=prod_of_cart.id_prod.id)
            #change the object
            prodToChange.countInStock = prodToChange.countInStock - prod_of_cart.QuantityProd
            prodToChange.nbr_purchase += prod_of_cart.QuantityProd
            prodToChange.save()
        # rendre cart empty
        for prod_to_drop in product_cart_to_buy:
            prod_to_drop.delete()
        cart_to_buy.GlobalPrice = 0
        cart_to_buy.save()
        messages.info(self.request, "Thanks for your purchase see you again")
        return redirect('acceuil')

class simpleCheckout(View):
    def get(self,request):
        return render(request,'simpleCheckout.html',{})
        

def ccomplete(request):
    return redirect("complete")

def OrderMail(request):
    print("########################### order mail################")
    address=ShipmentAddress.objects.get(cust=request.user.customer.id)
    orders = Order.objects.filter(cust=request.user.customer.id)
    nbrpurchase = Order.objects.filter(cust=request.user.customer).count()
    #print("###### nbrpurchase", nbrpurchase)
    total = Order.objects.filter(cust=request.user.customer).aggregate(r=Sum('TotalPrice'))
    #print("###### total", total['r'])
    for order in orders:
        ProdCartOrder = ProductCart.objects.filter(id=order.id_prodCart.id)
        #print('################ product cart order',ProdCartOrder)
        for Prod in ProdCartOrder:
            prodDB = Product.objects.filter(id=Prod.id_prod_id)
            #print('################ product order', prodDB)


    context = {'orders': orders, 'total':total['r'],'ProdCartOrder':ProdCartOrder, 'prodDB':prodDB,'address':address}

    html = render_to_string('email order.html', context)

    send_mail(
        'Purchase',
        'email order.html',
        'shopgamerfirst@gmail.com',
        [request.user.email],
        html_message =html,
        fail_silently=False,
    )
    print("########################### fin order mail################")

    return HttpResponse("azer")

def buy_cart(request):
    print("########################### buy cart################")
    # retrieve the cart want to buy
    cart_to_buy = Cart.objects.get(pk=request.user.customer.cart.id)
    # retrieve the productcart of the cart
    product_cart_to_buy = ProductCart.objects.filter(id_cart=cart_to_buy.id)
    # implementation de confirmation
    for prod_of_cart in product_cart_to_buy:
        # retrieve the specific product to change in db
        prodToChange = Product.objects.get(pk=prod_of_cart.id_prod.id)
        # change the object
        prodToChange.countInStock = prodToChange.countInStock - prod_of_cart.QuantityProd
        prodToChange.nbr_purchase += prod_of_cart.QuantityProd
        prodToChange.save()
    # emptycart
    for prod_to_drop in product_cart_to_buy:
        prod_to_drop.delete()
    cart_to_buy.GlobalPrice = 0
    cart_to_buy.save()
    print("########################### fin buy cart################")
    return HttpResponse("azer")

def createorder(request):
    print("########################### create order ################")
    product = ProductCart.objects.filter(id_cart=request.user.customer.cart.id)
    address = ShipmentAddress.objects.get(cust=request.user.customer)
    for prod in product:
        print("####################", prod.TotalPrice)
        Order.objects.create(id_cust=request.user.customer, id_prodCart=prod, address=address,
                             TotalPrice=prod.TotalPrice)
    print("########################### fin creeate order################")
    
    
    def Approve(request):
    product = ProductCart.objects.filter(id_cart=request.user.customer.cart.id, is_order=False)
    for prod in product:
        if prod.QuantityProd <= 0:
            prod.delete()
    cart_to_buy = Cart.objects.get(pk=request.user.customer.cart.id)
    cart_to_buy.GlobalPrice = 0
    cart_to_buy.save()
    messages = ("Sorry The Product No More Available")
    return render(request,'emptycart.html',{"messages":messages})

"""

