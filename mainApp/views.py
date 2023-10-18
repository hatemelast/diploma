from django.shortcuts import render, HttpResponseRedirect
from django.contrib.messages import success, error
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *

def homePage(Request):
    products = Product.objects.all().order_by("id")[0:12]
    return render(Request, "index.html", {"products": products})

def shopPage(Request, mc, sc, br):
    if mc == "All" and sc == "All" and br == "All":
        products = Product.objects.all().order_by("-id")
    elif mc != "All" and sc == "All" and br == "All":
        products = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc)
        ).order_by("-id")
    elif mc == "All" and sc != "All" and br == "All":
        products = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc)
        ).order_by("-id")
    elif mc == "All" and sc == "All" and br != "All":
        products = Product.objects.filter(
            brand=Brand.objects.get(name=br)
        ).order_by("-id")
    elif mc != "All" and sc != "All" and br == "All":
        products = (
            Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc),
                subcategory=Subcategory.objects.get(name=sc),
            )
            .order_by("-id")
            .order_by("-id")
        )
    elif mc != "All" and sc == "All" and br != "All":
        products = (
            Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc),
                brand=Brand.objects.get(name=br),
            )
            .order_by("-id")
            .order_by("-id")
        )
    elif mc == "All" and sc != "All" and br != "All":
        products = (
            Product.objects.filter(
                brand=Brand.objects.get(name=br),
                subcategory=Subcategory.objects.get(name=sc),
            )
            .order_by("-id")
            .order_by("-id")
        )
    else:
        products = (
            Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc),
                subcategory=Subcategory.objects.get(name=sc),
                brand=Brand.objects.get(name=br),
            )
            .order_by("-id")
            .order_by("-id")
        )

    maincategory = Maincategory.objects.all().order_by("-id")
    subcategory = Subcategory.objects.all().order_by("-id")
    brand = Brand.objects.all().order_by("-id")

    return render(
        Request,
        "shop.html",
        {
            "products": products,
            "maincategory": maincategory,
            "subcategory": subcategory,
            "brand": brand,
            "mc": mc,
            "sc": sc,
            "br": br,
        },
    )

def aboutPage(Request):
    return render(Request, "about.html")

def addtocartPage(Request):
    if (Request.method == "POST"):
        cart = Request.session.get("cart", None)
        qty = int(Request.POST.get("qty"))
        id = Request.POST.get("id")
        try:
            p = Product.objects.get(id=id)
            if (cart):
                if (str(id) in cart.keys()):
                    item = cart[str(id)]
                    item["qty"] = item["qty"] + qty
                    item["total"] = item["total"] + qty * item["price"]
                    cart[str(id)] = item
                else:
                    cart.setdefault(str(id), {
                        "product": id,
                        "name": p.name,
                        "brand": p.brand.name,
                        "color": p.color,
                        "size": p.size,
                        "price": p.finalprice,
                        "qty": qty,
                        "total": qty*p.finalprice,
                        "pic": p.pic1.url
                    })    
            else:
                cart = {str(id):{
                    "product": id,
                    "name": p.name,
                    "brand": p.brand.name,
                    "color": p.color,
                    "size": p.size,
                    "price": p.finalprice,
                    "qty": qty,
                    "total": qty*p.finalprice,
                    "pic": p.pic1.url
                }}

            Request.session["cart"] = cart
            Request.session.set_expiry(60*60*24*30)
        except:
            pass
    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def cartPage(Request):
    cart = Request.session.get("cart", None)
    subtotal = 0
    shipping = 0
    total = 0
    if (cart):
        for value in cart.values():
            subtotal= subtotal + value["total"]
        if (subtotal > 0 and subtotal < 1000):
            shipping = 150
        
        total = subtotal + shipping

    return render(Request, "cart.html", {
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })

def deletecartPage(Request,id):
    cart = Request.session.get("cart", None)
    if (cart):
        del cart[id]
        Request.session["cart"] = cart
        
    else:
        pass
    return HttpResponseRedirect("/cart/")

def updateCartPage(request, id, op):
    cart = request.session.get("cart", None)

    if cart and id in cart:
        item = cart[id]
        if op == "dec" and item["qty"] == 1:
            del cart[id]
        else:
            if op == "dec":
                item["qty"] = item["qty"] - 1
                item["total"] = item["total"] - item["price"]
            else:
                item["qty"] = item["qty"] + 1
                item["total"] = item["total"] + item["price"]

        request.session["cart"] = cart
    else:
        pass

    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def checkoutPage(Request):
    try:
        buyer = Buyer.objects.get(username=Request.user.username)
        cart = Request.session.get("cart", None)
        subtotal = 0
        shipping = 0
        total = 0
        if (cart):
            for value in cart.values():
                subtotal= subtotal + value["total"]
            if (subtotal > 0 and subtotal < 1000):
                shipping = 150
            total = subtotal + shipping

        if (Request.method =="POST"):
            Checkout = checkout()
            Checkout.buyer = buyer
            Checkout.subtotal = subtotal
            Checkout.total = total
            Checkout.shipping =shipping
            Checkout.save()

            for key,value in cart.items():
                p = Product.objects.get(id = int(key))
                cp = CheckoutProdcut()
                cp.Checkout = Checkout
                cp.product = p
                cp.qty = value["qty"]
                cp.total = value["total"]
                cp.save()

            Request.session["/cart/"] = {} 
            return HttpResponseRedirect("/confirmation/")    

        return render(Request,"checkout.html", {
            "buyer": buyer,
            "cart": cart,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total
        })
    except:
        return HttpResponseRedirect("/admin/")   

@login_required(login_url="/login/")
def confirmationPage(Request):
    return render(Request, "confirmation.html")

def contactPage(Request):
    return render(Request, "contact.html")

def loginPage(Request):
    if Request.method == "POST":
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(Request, user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            error(Request, "Invalid Username or Password!!!")
    return render(Request, "login.html")

def signupPage(Request):
    if Request.method == "POST":
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if password == cpassword:
            email = Request.POST.get("email")
            username = Request.POST.get("username")
            name = Request.POST.get("name")
            try:
                User.objects.create_user(
                    username = username, 
                    email = email, 
                    password = password, 
                    first_name = name
                )
                phone = Request.POST.get("phone")
                b = Buyer()
                b.name = name
                b.email = email
                b.username = username
                b.phone = phone
                b.save()
                return HttpResponseRedirect("/login/")
            except:
                error(Request, "UserName already taken!!!")
        else:
            error(Request, "Password and cofirm Password Doesn't Matched!!!")
    return render(Request, "signup.html")

@login_required(login_url="/login/")
def profilePage(Request):
    if Request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
    buyer = Buyer.objects.get(username=Request.user.username)
    wishlist = Wishlist.objects.filter(buyer=buyer)
    return render(Request, "profile.html", {
        "buyer": buyer, 
        "wishlist": wishlist
    })

@login_required(login_url="/login/")
def updateProfilePage(Request):
    if Request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
    buyer = Buyer.objects.get(username=Request.user.username)
    if Request.method == "POST":
        buyer.name = Request.POST.get("name")
        buyer.email = Request.POST.get("email")
        buyer.phone = Request.POST.get("phone")
        buyer.address = Request.POST.get("address")
        buyer.city = Request.POST.get("city")
        buyer.state = Request.POST.get("state")
        if Request.FILES.get("pic"):
            buyer.pic = Request.FILES.get("pic")
        buyer.save()
        return HttpResponseRedirect("/profile")
    return render(Request, "update-profile.html", {
        "buyer": buyer
    })

def singleProduct(Request, id):
    product = Product.objects.get(id=id)
    return render(Request, "single-product.html", {
        "product": product
    })

@login_required(login_url="/login/")
def addtowishlistPage(Request, id):
    buyer = Buyer.objects.get(username=Request.user.username)
    product = Product.objects.get(id=id)
    try:
        w = Wishlist.objects.get(product=product, buyer=buyer)
    except:
        w = Wishlist()
        w.product = product
        w.buyer = buyer
        w.save()
    return HttpResponseRedirect("/profile")

def addtoCardPage(Request, id):
    if (Request.method == "GET"):
        cart = Request.session.get("cart", None)
        try:
            p = Product.objects.get(id=id)
            if (cart):
                if (str(id) in cart.keys()):
                    item = cart[str(id)]
                    item["qty"] = item["qty"] + 1
                    item["total"] = item["total"] + 1 * item["price"]
                    cart[str(id)] = item
                else:
                    cart.setdefault(str(id), {
                        "product": id,
                        "name": p.name,
                        "brand": p.brand.name,
                        "color": p.color,
                        "size": p.size,
                        "price": p.finalprice,
                        "qty": 1,
                        "total": 1 * p.finalprice,
                        "pic": p.pic1.url
                    })    
            else:
                cart = {str(id):{
                    "product": id,
                    "name": p.name,
                    "brand": p.brand.name,
                    "color": p.color,
                    "size": p.size,
                    "price": p.finalprice,
                    "qty": 1,
                    "total": 1 * p.finalprice,
                    "pic": p.pic1.url
                }}

            Request.session["cart"] = cart
            Request.session.set_expiry(60*60*24*30)
        except:
            pass
    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def deletewishlist(Request, id):
    try:
        w = Wishlist.objects.get(id=id)
        w.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")

def logoutPage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")