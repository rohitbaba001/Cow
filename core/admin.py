from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User, Worker, Task, Cow, Doctor, VeterinaryVisit, 
                     Medicine, ArtificialInsemination, Pregnancy, Vaccination)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_staff', 'created_at']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address')}),
    )


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'date_of_joining', 'is_active']
    list_filter = ['is_active', 'date_of_joining']
    search_fields = ['employee_id', 'user__username', 'user__first_name', 'user__last_name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'assigned_by', 'deadline', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'deadline']
    search_fields = ['title', 'description', 'assigned_to__user__username']
    date_hierarchy = 'created_at'


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ['cow_number', 'cow_name', 'breed', 'age', 'health_status', 'is_active', 'created_at']
    list_filter = ['breed', 'health_status', 'is_active']
    search_fields = ['cow_number', 'cow_name', 'breed']
    date_hierarchy = 'created_at'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'qualification', 'license_number', 'phone_number', 'is_active']
    list_filter = ['is_active', 'specialization']
    search_fields = ['name', 'license_number', 'phone_number']


@admin.register(VeterinaryVisit)
class VeterinaryVisitAdmin(admin.ModelAdmin):
    list_display = ['cow', 'doctor', 'visit_date', 'visit_type', 'recorded_by']
    list_filter = ['visit_type', 'visit_date']
    search_fields = ['cow__cow_number', 'doctor__name', 'reason_for_visit']
    date_hierarchy = 'visit_date'


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'visit', 'dosage', 'frequency', 'start_date', 'end_date']
    list_filter = ['start_date']
    search_fields = ['medicine_name', 'visit__cow__cow_number']


@admin.register(ArtificialInsemination)
class ArtificialInseminationAdmin(admin.ModelAdmin):
    list_display = ['cow', 'ai_date', 'bull_breed', 'doctor', 'success_status']
    list_filter = ['success_status', 'ai_date']
    search_fields = ['cow__cow_number', 'bull_breed', 'bull_id']
    date_hierarchy = 'ai_date'


@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ['cow', 'pregnancy_status', 'confirmation_date', 'expected_delivery_date', 'actual_delivery_date']
    list_filter = ['pregnancy_status', 'confirmation_date']
    search_fields = ['cow__cow_number']
    date_hierarchy = 'confirmation_date'


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['cow', 'vaccine_name', 'vaccination_date', 'next_due_date', 'administered_by']
    list_filter = ['vaccination_date', 'vaccine_name']
    search_fields = ['cow__cow_number', 'vaccine_name']
    date_hierarchy = 'vaccination_date'
