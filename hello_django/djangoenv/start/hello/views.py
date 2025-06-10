from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.db.models import F
import datetime
import pytz
import logging
from django.utils import timezone
import requests
import collections
from django.views import View
from .forms import UserForm
from .models import *
import statistics
import os
import matplotlib.pyplot as plt
from django.conf import settings
from django.db.models import Count
from .models import Order 
from datetime import date, timedelta
logging.basicConfig(level=logging.INFO, filename="my_log.log",filemode="a",format="%(asctime)s %(levelname)s %(message)s")

def stats(request):
    print("HERE1")
    # Получаем дату 7 дней назад от сегодня
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=6)  # Чтобы считать 7 дней включая сегодня

    # Получаем количество заказов для каждого дня за последние 7 дней
    orders_per_day = (
        Order.objects.filter(ordering_time__date__gte=seven_days_ago, ordering_time__date__lte=today)
        .values('ordering_time__date')
        .annotate(count=Count('id'))
        .order_by('ordering_time__date')
    )

    # Создаем словарь дата -> количество, чтобы заполнить пропуски (если в какой-то день заказов не было)
    orders_dict = {entry['ordering_time__date']: entry['count'] for entry in orders_per_day}

    # Подготавливаем данные для графика: список дат и количество заказов
    dates = [seven_days_ago + datetime.timedelta(days=i) for i in range(7)]
    counts = [orders_dict.get(date, 0) for date in dates]

    # Форматируем даты для отображения на оси X (например, '01 Jun')
    x_labels = [date.strftime('%d %b') for date in dates]

    # Рисуем график
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x_labels, counts, color='skyblue')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Количество заказов')
    ax.set_title('Количество новых заказов за последние 7 дней')

    # Сохраняем график в PNG в папку media
    graph_path = os.path.join(settings.MEDIA_ROOT, 'orders_last_7_days.png')
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    plt.savefig(graph_path)
    plt.close(fig)  # Закрываем фигуру, чтобы не держать память

    context = {
    'plot_url': settings.MEDIA_URL + 'orders_last_7_days.png'
    }
    print("HERE2")
    return render(request, 'stats.html', context)

def main(request):
    services = Service.objects.all()
    
    url = "https://catfact.ninja/fact"
    response = requests.get(url).json()

    # Получаем прямую ссылку на картинку кота через TheCatAPI
    cat_response = requests.get("https://api.thecatapi.com/v1/images/search").json()
    cat_img_url = cat_response[0]["url"]

    article = Article()
    article.text = response["fact"]
    article.img_url = cat_img_url
    article.title = f"Random Cat Fact - {datetime.datetime.now()}"
    
    try:
        article.save()
        logging.info(f"{article.title} is saved.")
    except:
        logging.warning(f"{article.title} cannot be saved.")

    article = Article.objects.order_by("created_at").last()

    # Получение текущей даты для пользователя и UTC
    utc_now = datetime.datetime.now(tz=pytz.utc)

    if request.method == "POST":
        price_from = int(request.POST.get('price_from'))
        price_to = int(request.POST.get('price_to'))
        if price_from > price_to:
            return HttpResponse("Filter is not correct.")
        services = services.filter(price__gte=price_from)
        services = services.filter(price__lte=price_to)
    return render(request, "main.html", {"services" : services, "article" : article,
                                         "user_now": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                                         "utc_now": utc_now.strftime('%d/%m/%Y %H:%M:%S'),})



#Диаграмма matplot
#login
#дата рождения
#меню для каждой страницы
#рейтинг в отзывах

import os
import datetime
import statistics
import collections
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render
from .models import Client, Order  # Импортируй свои модели

def statisticsv(request):
    clients = Client.objects.all()

    # Расчёт возраста клиентов
    sum_age = 0
    years = []
    for cl in clients:
        age = datetime.date.today().year - cl.age.year
        years.append(age)
        sum_age += age
    avg_age = round(sum_age / len(years), 2) if years else 0
    median_age = statistics.median(years) if years else 0

    # Расчёт средней, медианной, моды по цене продаж
    sum_price = 0
    sale_prices = []
    for cl in clients:
        sum_price += cl.result_price
        sale_prices.append(cl.result_price)
    avg_sale_price = round(sum_price / len(clients), 2) if clients else 0
    median_sale_price = statistics.median(sale_prices) if sale_prices else 0
    mode_sale_price = statistics.mode(sale_prices) if sale_prices else 0

    alphabet_clients = Client.objects.order_by("name")
    whole_sale_price = round(sum_price, 2)

    orders = Order.objects.all()
    order_services = [o.service for o in orders]
    service_counts = collections.Counter(order_services)
    most_common_service = max(service_counts, key=service_counts.get) if service_counts else None

    # Подсчёт заказов за последние 7 дней по ordering_time
    today = now().date()
    orders_last_7_days = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        count = Order.objects.filter(ordering_time__date=day).count()
        orders_last_7_days.append(count)

    # Построение графика
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(orders_last_7_days, marker='o')
    ax.set_title("Orders Last 7 Days")
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Orders")
    ax.grid(True)

    graph_filename = 'orders_last_7_days.png'
    graph_path = os.path.join(settings.MEDIA_ROOT, graph_filename)
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    fig.savefig(graph_path)
    plt.close(fig)

    plot_url = settings.MEDIA_URL + graph_filename

    context = {
        "average_age": avg_age,
        "median_age": median_age,
        "average_sale_price": avg_sale_price,
        "median_sale_price": median_sale_price,
        "mode_sale_price": mode_sale_price,
        "sorted_clients": alphabet_clients,
        "whole_sale_price": whole_sale_price,
        "most_common_service": most_common_service,
        "plot_url": plot_url,
    }

    return render(request, "statistics.html", context)

def about_company(request):
    return render(request, "about_company.html")

def contacts(request):
    return render(request, "contacts.html", {"masters" : Master.objects.all()})

#сортировка
def news(request):
    artcs = Article.objects.all()
    if request.method == "POST":
        val = request.POST.get("sort")
        if val == "date_new":
            artcs = Article.objects.order_by("created_at").reverse()
        elif val == "date_old":
            artcs = Article.objects.order_by("created_at")
        return render(request, "news.html", {"articles" : artcs})
    return render(request, "news.html", {"articles" : artcs})

def politics(request):
    return render(request, "politics.html")

#поиск
def promocodes(request):
    proms = Promocode.objects.all()
    sprom = None
    if request.method == "POST":
        tname = request.POST.get("search_term")
        if Promocode.objects.filter(name = tname).exists():
            sprom = Promocode.objects.filter(name = tname)
            return render(request, "promocodes.html", {"proms" : proms, "searched" : sprom})
    return render(request, "promocodes.html", {"proms" : proms, "searched" : sprom})

def qa(request):
    qas = QA.objects.all()
    return render(request, "qa.html", {"qas" : qas})

def reviews(request):
    if request.method == "POST":
        return render(request, "register.html", {'specializations' : Specialization.objects.all()})
    return render(request, "reviews.html", {"reviews" : Review.objects.order_by("date").reverse()})

def vacancies(request):
    return render(request, "vacancies.html", {"jobs" : Job.objects.all()})

def login(request):
    userform = UserForm()
    if request.method == "POST":
        userform = UserForm(request.POST)
        if not userform.is_valid():
            tlogin = request.POST.get("login")
            tpassword = request.POST.get("password")
            usertype = request.POST.get("user_type")
            
            if usertype == "master":
                searched_masters = MasterCredentials.objects.filter(login = tlogin)
                if len(searched_masters) > 0:
                    searched_masters = searched_masters.filter(password = tpassword)
                    if len(searched_masters) == 1:
                        logging.info(f"Master {searched_masters.first().master.name} added.")
                        return redirect(f'master/{searched_masters.first().master.pk}')
                    else:
                        logging.warning(f"Master not found.")
                        return HttpResponseNotFound("Invalid password")
                else:
                    logging.warning(f"Master not found.")
                    return HttpResponseNotFound("No master with this login found")
            else:
                searched_clients = ClientCredentials.objects.filter(login = tlogin)
                if len(searched_clients) > 0:
                    searched_clients = searched_clients.filter(password = tpassword)
                    if len(searched_clients) == 1:
                        logging.info(f"Client {searched_clients.first().client.name} added.")
                        return redirect(f'client/{searched_clients.first().client.pk}')
                    else:
                        logging.warning(f"Client not found.")
                        return HttpResponseNotFound("Invalid password")
                else:
                    logging.warning(f"Client not found.")
                    return HttpResponseNotFound("No client with this login found")
        else:
            return HttpResponse("Invalid data")
    else:
        return render(request, "login.html", { "form" : userform })


def CheckAge(age):
    min_birthday = datetime.date.today() - datetime.timedelta(days=365*18)
    if min_birthday < age:
        return False
    return True


def register(request):
    userform = UserForm()
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            tpassword = request.POST.get("password")
            tlogin = request.POST.get("login")
            name = request.POST.get("name")
            age = request.POST.get("date_of_birth")
            tphone_number = "+375 (" + request.POST.get("phone_code") + ") " + request.POST.get("phone_number")
            usertype = request.POST.get("user_type")

            dob = datetime.datetime.strptime(age, "%Y-%m-%d").date()

            is_adult = CheckAge(dob)
            if is_adult == False:
                return HttpResponse("You must be 18+ y/o.")
            
            if usertype == "master":
                if MasterCredentials.objects.filter(login = tlogin).exists():
                    return HttpResponse("Master with this login already exists.")
                new_master = Master()
                new_master.name = name
                new_master.age = age
                new_master.phone_number = tphone_number
                new_master.order_count = 0
                new_master.specialization = Specialization.objects.first()
                new_master.save()
                new_master_cred = MasterCredentials()
                new_master_cred.master = new_master
                new_master_cred.login = tlogin
                new_master_cred.password = tpassword
                new_master_cred.save()
                return redirect(f'master/{new_master.pk}')
            else:
                if ClientCredentials.objects.filter(login = tlogin).exists():
                    return HttpResponse("Client with this login already exists.")
                new_client = Client()
                new_client.name = name
                new_client.age = age
                new_client.phone_number = tphone_number
                new_client.result_price = 0
                new_client.car_model = CarModel.objects.first()
                new_client.car_type = CarType.objects.first()
                new_client.save()
                new_cl_creds = ClientCredentials()
                new_cl_creds.client = new_client
                new_cl_creds.login = tlogin
                new_cl_creds.password = tpassword
                new_cl_creds.save()
                return redirect(f'client/{new_client.pk}')
        else:
            return HttpResponse("Invalid data")
    else:
        return render(request, "register.html", {'specializations' : Specialization.objects.all(),
                                                 "form" : userform})
    
    

def mastersview(request, master_id):
    mast = Master.objects.get(id = master_id)
    clients_id = ClientMaster.objects.filter(master = mast)
    clients = set(cm.client for cm in clients_id)
    return render(request, "master.html", {"master": mast, "master_id" : master_id, "specs" : Specialization.objects.all(),
                                           "orders" : Order.objects.filter(master = mast),
                                           "clients" : clients})

def clientsview(request, client_id):
    client = Client.objects.get(id = client_id)
    return render(request, "client.html", {"client": client, 
                                           "client_id" : client_id, 
                                           "car_models" : CarModel.objects.all(), 
                                           "car_types" : CarType.objects.all(),
                                           "proms" : Promocode.objects.all(),
                                           "reviews" : Review.objects.filter(user = client).order_by("date").reverse()})


def editmaster(request, master_id):
    mast = Master.objects.get(id=master_id)
    error = None
    if request.method == "POST":
        tname = request.POST.get("name")
        tage = request.POST.get("age")
        tphone_code = request.POST.get("phone_code")
        tphone_number = request.POST.get("phone_number")
        tspecialization = request.POST.get("specialization")
        photo_file = request.FILES.get("photo")

        if tname:
            mast.name = tname
        if tage:
            mast.age = tage
        if tphone_code and tphone_number:
            mast.phone_number = f"+375 ({tphone_code}) {tphone_number}"
        if tspecialization:
            mast.specialization_id = tspecialization
        if photo_file:
            mast.photo = photo_file
        mast.save()
        return redirect('master', master_id=master_id)
    return render(request, "editmaster.html", {"master": mast, "specs": Specialization.objects.all(), "error": error})

def editclient(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == "POST":
        tname = request.POST.get("name")
        tage = request.POST.get("age")
        tphone_code = request.POST.get("phone_code")
        tphone_number = request.POST.get("phone_number")
        tmodel = request.POST.get("model_car")
        ttype = request.POST.get("type_car")
        photo_file = request.FILES.get("photo")

        if tname:
            client.name = tname
        if tage:
            client.age = tage
        if tphone_code and tphone_number:
            client.phone_number = f"+375 ({tphone_code}) {tphone_number}"
        if tmodel:
            client.car_model_id = tmodel
        if ttype:
            client.car_type_id = ttype
        if photo_file:
            client.photo = photo_file
        client.save()
        return redirect('client', client_id=client_id)
    else:
        return render(request, "editclient.html", {"client": client, "car_models": CarModel.objects.all(), "car_types": CarType.objects.all()})
    

def createorder(request, client_id):
    client = Client.objects.get(id = client_id)
    if request.method == "POST":
        order = Order()
        order.master = Master.objects.get(id = request.POST.get("master"))
        order.client = client
        order.ordering_time = datetime.datetime.now()
        order.service = Service.objects.get(id = request.POST.get("service"))
        selected_parts = Part.objects.filter(id__in=request.POST.getlist("parts"))
        prom = None
        if request.POST.get("promocode"):
            try:
                prom = Promocode.objects.get(name = request.POST.get("promocode"))
            except:
                prom = None
        if prom is None:
            order.whole_price = order.CountPrice(parts=selected_parts)
        else:
            order.whole_price = order.CountPrice(prom,selected_parts)
        order.save()
        Client.objects.filter(id = client_id).update(result_price=F('result_price') + order.whole_price)
        Master.objects.filter(id = order.master.pk).update(order_count=F('order_count') + 1)
        master = Master.objects.get(id = order.master.pk)
        client = Client.objects.get(id = client_id)
        new_clientmaster = ClientMaster()
        new_clientmaster.client = client
        new_clientmaster.master = master
        new_clientmaster.save()
        return redirect('client',client_id = client.pk)
    else:
        return render(request,"createorder.html", {"client_id" : client_id, 
                                                   "masters" : Master.objects.all(), 
                                                   "services" : Service.objects.all(), 
                                                   "parts" : Part.objects.filter(car_model = client.car_model)})
    

def createreview(request, client_id):
    user = Client.objects.get(id = client_id)
    if request.method == "POST":
        ttext = request.POST.get("text")
        trating = request.POST.get("rating")
        new_review = Review()
        new_review.user = user
        new_review.text = ttext
        new_review.rating = int(trating)
        new_review.save()
        return redirect('client',client_id = user.pk)
    else:
        return render(request,"createreview.html")
    
def editreview(request, client_id, review_id):
    user = Client.objects.get(id = client_id)
    review = Review.objects.get(id = review_id)
    if request.method == "POST":
        ttext = request.POST.get("text")
        trating = request.POST.get("rating")

        Review.objects.filter(id = review_id).update(text = ttext)
        Review.objects.filter(id = review_id).update(rating = int(trating))
        return redirect('client',client_id = user.pk)
    else:
        return render(request,"editreview.html", {"review" : review})
    
def deletereview(request, client_id, review_id):
    user = Client.objects.get(id = client_id)
    review = Review.objects.get(id = review_id)
    if request.method == "POST":
        review.delete()
        return redirect('client',client_id = user.pk)
    else:
        return render(request,"deletereview.html", {"review" : review})
    

def recreate_articles_with_cats():
    from hello.models import Article
    import requests, datetime, logging
    Article.objects.all().delete()
    for _ in range(5):
        fact = requests.get("https://catfact.ninja/fact").json()["fact"]
        cat_img_url = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]
        article = Article()
        article.text = fact
        article.img_url = cat_img_url
        article.title = f"Random Cat Fact - {datetime.datetime.now()}"
        article.save()
        logging.info(f"{article.title} is saved.")

    