from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-language/', views.change_language, name='change_language'),
    
    # Worker Management
    path('workers/', views.worker_list, name='worker_list'),
    path('workers/create/', views.worker_create, name='worker_create'),
    path('workers/<int:pk>/delete/', views.worker_delete, name='worker_delete'),
    
    # Task Management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    
    # Cow Management
    path('cows/', views.cow_list, name='cow_list'),
    path('cows/create/', views.cow_create, name='cow_create'),
    path('cows/<int:pk>/', views.cow_detail, name='cow_detail'),
    path('cows/<int:pk>/update/', views.cow_update, name='cow_update'),
    path('cows/<int:pk>/delete/', views.cow_delete, name='cow_delete'),
    
    # Veterinary System
    path('veterinary/', views.veterinary_dashboard, name='veterinary_dashboard'),
    
    # Doctor Management
    path('veterinary/doctors/', views.doctor_list, name='doctor_list'),
    path('veterinary/doctors/create/', views.doctor_create, name='doctor_create'),
    path('veterinary/doctors/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    
    # Veterinary Visits
    path('veterinary/visits/<int:cow_id>/create/', views.visit_create, name='visit_create'),
    path('veterinary/visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    
    # Medicines
    path('veterinary/visits/<int:visit_id>/medicine/create/', views.medicine_create, name='medicine_create'),
    
    # Artificial Insemination
    path('veterinary/ai/', views.ai_list, name='ai_list'),
    path('veterinary/ai/create/', views.ai_create, name='ai_create'),
    path('veterinary/ai/<int:cow_id>/create/', views.ai_create, name='ai_create_for_cow'),
    path('veterinary/ai/<int:pk>/', views.ai_detail, name='ai_detail'),
    
    # Pregnancy
    path('veterinary/pregnancy/', views.pregnancy_list, name='pregnancy_list'),
    path('veterinary/pregnancy/create/', views.pregnancy_create, name='pregnancy_create'),
    path('veterinary/pregnancy/<int:cow_id>/create/', views.pregnancy_create, name='pregnancy_create_for_cow'),
    path('veterinary/pregnancy/<int:pk>/update/', views.pregnancy_update, name='pregnancy_update'),
    
    # Vaccination
    path('veterinary/vaccination/', views.vaccination_list, name='vaccination_list'),
    path('veterinary/vaccination/create/', views.vaccination_create, name='vaccination_create'),
    path('veterinary/vaccination/<int:cow_id>/create/', views.vaccination_create, name='vaccination_create_for_cow'),
]
