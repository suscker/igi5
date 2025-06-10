from django.test import TestCase
from .models import *

class PartTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        cls.car_model = CarModel.objects.create(name="Toyota Corolla")
        cls.part_type = PartType.objects.create(name="Engine")
        cls.part = Part.objects.create(name="Piston", car_model=cls.car_model, price=100, type=cls.part_type)

    def test_part_creation(self):
        print("Method: test_part_creation.")
        self.assertEqual(self.part.name, "Piston")
        self.assertEqual(self.part.car_model, self.car_model)
        self.assertEqual(self.part.price, 100)
        self.assertEqual(self.part.type, self.part_type)

    def test_part_string_representation(self):
        print("Method: test_part_string_representation.")
        self.assertEqual(str(self.part), "Piston")

class PromocodeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        cls.promocode = Promocode.objects.create(name="SUMMER10", discount=10)

    def test_promocode_creation(self):
        print("Method: test_promocode_creation.")
        self.assertEqual(self.promocode.name, "SUMMER10")
        self.assertEqual(self.promocode.discount, 10)

    def test_promocode_string_representation(self):
        print("Method: test_promocode_string_representation.")
        self.assertEqual(str(self.promocode), "SUMMER10")

class OrderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        cls.car_model = CarModel.objects.create(name="Toyota Corolla")
        cls.part_type = PartType.objects.create(name="Engine")
        cls.part = Part.objects.create(name="Piston", car_model=cls.car_model, price=100, type=cls.part_type)
        cls.master = Master.objects.create(name="John Doe")
        cls.client = Client.objects.create(name="Jane Smith")
        cls.service = Service.objects.create(name="Engine Repair", price=200)
        cls.order = Order.objects.create(master=cls.master, client=cls.client, whole_price=300, ordering_time="2023-01-01 10:00:00", service=cls.service)

    def test_order_creation(self):
        print("Method: test_order_creation.")
        self.assertEqual(self.order.master, self.master)
        self.assertEqual(self.order.client, self.client)
        self.assertEqual(self.order.whole_price, 300)
        self.assertEqual(str(self.order.ordering_time), "2023-01-01 10:00:00+00:00")
        self.assertEqual(self.order.service, self.service)

    def test_count_price_without_promocode(self):
        print("Method: test_count_price_without_promocode.")
        parts = [self.part]
        price = self.order.CountPrice(parts=parts)
        self.assertEqual(price, 300)

    def test_count_price_with_promocode(self):
        print("Method: test_count_price_with_promocode.")
        parts = [self.part]
        promocode = Promocode.objects.create(name="SUMMER10", discount=10)
        price = self.order.CountPrice(prom=promocode, parts=parts)
        self.assertEqual(price, 270)

class ServiceTypeTestCase(TestCase):
    def test_service_type_creation(self):
        service_type = ServiceType.objects.create(name="Oil change")
        self.assertEqual(str(service_type), "Oil change")

class ServiceTestCase(TestCase):
    def test_service_creation(self):
        service_type = ServiceType.objects.create(name="Oil change")
        service = Service.objects.create(name="Full oil change", price=50, type=service_type)
        self.assertEqual(str(service), "Full oil change")

class CarModelTestCase(TestCase):
    def test_car_model_creation(self):
        car_model = CarModel.objects.create(name="Audi")
        self.assertEqual(str(car_model), "Audi")

class CarTypeTestCase(TestCase):
    def test_car_type_creation(self):
        car_type = CarType.objects.create(name="Sedan")
        self.assertEqual(str(car_type), "Sedan")

class ClientTestCase(TestCase):
    def test_client_creation(self):
        car_model = CarModel.objects.create(name="BMW")
        car_type = CarType.objects.create(name="Coupe")
        client = Client.objects.create(name="John Doe", age=25, phone_number="+375 (44) 123-45-67", result_price=100, car_model=car_model, car_type=car_type)
        self.assertEqual(str(client), "John Doe")

class SpecializationTestCase(TestCase):
    def test_specialization_creation(self):
        specialization = Specialization.objects.create(name="Engine repair")
        self.assertEqual(str(specialization), "Engine repair")

class MasterTestCase(TestCase):
    def test_master_creation(self):
        specialization = Specialization.objects.create(name="Engine repair")
        master = Master.objects.create(name="Jane Smith", age=30, phone_number="+375 (33) 987-65-43", specialization=specialization, order_count=10)
        self.assertEqual(str(master), "Jane Smith")
        self.assertIsNone(master.photo)

class PartTypeTestCase(TestCase):
    def test_part_type_creation(self):
        part_type = PartType.objects.create(name="Brake pads")
        self.assertEqual(str(part_type), "Brake pads")