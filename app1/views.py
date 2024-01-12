from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app1.models import Product, SubscriptionLevel
import logic
from pathlib import Path
from django.http import HttpResponseForbidden
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from AICG.settings import BASE_DIR
import requests


def cpationgen(image_path):
    api_url = "http://127.0.0.5:8000/predict-caption"

    with open(image_path, "rb") as image_file:

        files = {"file": (image_path, image_file, "image/jpeg")}

        response = requests.post(api_url, files=files)

        if response.status_code == 200:

            data = response.json()
            predicted_caption = data.get("predicted_caption")

            return predicted_caption
        else:
            return response.text


@login_required(login_url="login")
def home_page(request):
    if request.method == "POST":

        uploaded_file = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        image_path = fs.save("test.jpg", uploaded_file)

        print(image_path)
        request.session['image_path'] = image_path

        return redirect("caption")

    latest_subscription = SubscriptionLevel.objects.filter(
        user=request.user)
    latest_subscription = latest_subscription.latest("purchase_date")
    credits_left = latest_subscription.credit_left

    return render(request, 'home.html', {"credits": credits_left})


@login_required(login_url="login")
def caption_page(request):

    image_path = request.session.get('image_path')

    image_pathx = os.path.join(settings.BASE_DIR, "media", image_path)

    if not image_path:
        return HttpResponseForbidden("Image path not found. Please upload an image first.")

    if request.user.is_authenticated:

        latest_subscription = SubscriptionLevel.objects.filter(
            user=request.user)
        latest_subscription = latest_subscription.latest("purchase_date")

        if latest_subscription.credit_left > 0:

            latest_subscription.credit_left -= 1
            latest_subscription.save()

            caption = cpationgen(image_pathx)

            return render(request, "caption.html", {"caption": caption, "img": image_path})
        else:
            return HttpResponseForbidden("Insufficient credits. Please purchase more credits.")
    else:
        return HttpResponseForbidden("User not authenticated.")


def login_form(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect("home")
        else:
            return HttpResponse("The User name and password is incorrect")

    return render(request, "login.html")


def signup_form(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")

        if password1 != password2:
            return HttpResponse("Your password is not the same")

        myuser = User.objects.create_user(
            username=username, email=email, password=password1)
        myuser.save()

        free_product = Product.objects.get(product_id=00)
        SubscriptionLevel.objects.create(
            subscribed_product=free_product,
            credit_left=free_product.credit_grant,
            user=myuser
        )

        return redirect("login")

    return render(request, "signup.html")


def logout_page(request):
    logout(request=request)
    return redirect("login")


def purchase_page(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        user = request.user
        product = Product.objects.get(product_id=product_id)
        latest_subscription = SubscriptionLevel.objects.filter(
            user=request.user)
        latest_subscription = latest_subscription.latest("purchase_date")

        credits_left = latest_subscription.credit_left
        SubscriptionLevel.objects.create(
            subscribed_product=product,
            credit_left=credits_left + product.credit_grant,
            user=user
        )
        return redirect("home")
    products = Product.objects.exclude(product_id='00')

    return render(request, "purchase.html", {"products": products})


def show_history(request):
    user = request.user
    history = SubscriptionLevel.objects.filter(user=user)
    return render(request, "history.html", {"history": history})
