from django.contrib import admin
from .models import *

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(CarModel)
admin.site.register(CarType)
admin.site.register(Specialization)
admin.site.register(Client)
admin.site.register(Master)
admin.site.register(ClientCredentials)
admin.site.register(MasterCredentials)
admin.site.register(Promocode)
admin.site.register(Order)
admin.site.register(ClientMaster)
admin.site.register(QA)
admin.site.register(Job)
admin.site.register(Review)
admin.site.register(Article)
admin.site.register(PartnerCompany)
admin.site.register(CompanyInfo)
admin.site.register(Term)
admin.site.register(StaffMember)

class PartTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = ['display_parts_by_type']

    def display_parts_by_type(self, request, queryset):
        """
        Custom action to display parts of a specific type.
        """
        part_type = queryset.first()
        parts = Part.objects.filter(type=part_type)

        if parts:
            self.message_user(request, f"Parts of type '{part_type.name}':")
            for part in parts:
                self.message_user(request, f"- Part: {part.name}, Car_model: {part.car_model.name}, Price: {part.price}")
        else:
            self.message_user(request, f"No parts found of type '{part_type.name}'.")

    display_parts_by_type.short_description = "Display parts by type"

admin.site.register(PartType, PartTypeAdmin)
# Part уже зарегистрирован выше? Регистрируем только один раз.
# admin.site.register(Part)

admin.site.register(Banner)