from django.db import models
from django.utils.timezone import now


#Тип услуг
class ServiceType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
#Услуга
class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    type = models.ForeignKey(ServiceType, related_name="services", on_delete=models.CASCADE)

    def __str__(self):
        return self.name



#ex: audi, bmw
class CarModel(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

#Тип авто
class CarType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


#Специализация мастеров
class Specialization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

#Клиент
class Client(models.Model):
    name = models.CharField(max_length=30)
    age = models.DateField()
    phone_number = models.CharField(max_length=19) # +375 (44) xxx-xx-xx
    result_price = models.PositiveIntegerField() #for promocode
    car_model = models.ForeignKey(CarModel, related_name="clients", on_delete=models.DO_NOTHING)
    car_type = models.ForeignKey(CarType, related_name="clients", on_delete=models.DO_NOTHING)
    photo = models.ImageField(upload_to='clients_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

#Мастер
class Master(models.Model):
    name = models.CharField(max_length=30)
    age = models.DateField()
    phone_number = models.CharField(max_length=19)
    specialization = models.ForeignKey(Specialization, related_name="masters", on_delete=models.CASCADE,  default=None)
    order_count = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='masters_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class ClientCredentials(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True)
    login = models.CharField(max_length=20, default="login")
    password = models.CharField(max_length=20, default="password")


class MasterCredentials(models.Model):
    master = models.OneToOneField(Master, on_delete=models.CASCADE, primary_key=True)
    login = models.CharField(max_length=20, default="login")
    password = models.CharField(max_length=20, default="password")


#Вид запчастей
class PartType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

#Запчасть
class Part(models.Model):
    name = models.CharField(max_length=20)
    car_model = models.ForeignKey(CarModel, related_name="parts", on_delete=models.CASCADE, default=None)
    price = models.PositiveIntegerField()
    type = models.ForeignKey(PartType, related_name="parts", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


#Промокод
class Promocode(models.Model):
    name = models.CharField(max_length=15)
    discount = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    expires_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

#Заказ
class Order(models.Model):
    master = models.ForeignKey(Master, related_name="orders", on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(Client, related_name="orders", on_delete=models.CASCADE, default=None)
    whole_price = models.PositiveIntegerField()
    ordering_time = models.DateTimeField()
    service = models.ForeignKey(Service, related_name="orders", on_delete=models.DO_NOTHING)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    def CountPrice(self, prom = None, parts = None):
        price = self.service.price
        if parts:
            for p in parts:
                price += p.price
        if prom:
            price *= 0.01*(100-prom.discount)
        return price


class ClientMaster(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)



class QA(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date = models.DateField(default=now)


class Job(models.Model):
    title = models.CharField(max_length=50)
    salary = models.IntegerField()
    description = models.TextField()

#добавить рейтинг
class Review(models.Model):
    user = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5)


class Article(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField()
    summary = models.CharField(max_length=200, default='', blank=True)
    img_url = models.CharField(max_length=500, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PartnerCompany(models.Model):
    name = models.CharField(max_length=100)
    website_url = models.URLField()
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)

    def __str__(self):
        return self.name


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100, default='Наша компания')
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    history = models.TextField(blank=True)
    requisites = models.TextField(blank=True)
    certificate_text = models.TextField(blank=True, default='СВИДЕТЕЛЬСТВО\n\nо предоставлении услуг автосервиса\n\nг. [Город]\n"[Дата]"\n\nНастоящим удостоверяется, что\n\nАвтосервис "[Название компании]"\n(ИНН [номер], ОГРН [номер])\n\nвнесен в реестр сервисных организаций и имеет право оказывать услуги по:\n\nтехническому обслуживанию автомобилей,\n\nдиагностике и ремонту,\n\nгарантийному и постгарантийному обслуживанию.\n\nРегистрационный номер: [XXXX]\n\nПодпись руководителя _____________\nМ.П.')

    def __str__(self):
        return self.name


class Term(models.Model):
    term = models.CharField(max_length=100)
    definition = models.TextField()
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.term


class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} — {self.role}"


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    alt_text = models.CharField(max_length=200, blank=True, default='')
    target_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.alt_text or f"Banner #{self.pk}"


