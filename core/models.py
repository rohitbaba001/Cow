from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User Model"""
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('worker', 'Worker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='worker')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Worker(models.Model):
    """Worker Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"


class Task(models.Model):
    """Task Assignment Model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    notes = models.TextField(blank=True, null=True, help_text='Additional instructions or notes')
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.assigned_to.user.username}"
    
    def is_overdue(self):
        if self.status != 'completed' and self.deadline < timezone.now():
            return True
        return False


class Cow(models.Model):
    """Cow/Cattle Management Model for Veterinary Section"""
    cow_number = models.CharField(max_length=50, unique=True, help_text='Unique identification number')
    cow_name = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100)
    age = models.IntegerField(help_text='Age in years')
    color = models.CharField(max_length=50)
    identification_mark = models.TextField(help_text='Special identification marks or features')
    health_status = models.CharField(max_length=100, default='Healthy')
    last_checkup = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='cows/', blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['cow_number']
    
    def __str__(self):
        return f"{self.cow_number} - {self.cow_name or 'Unnamed'}"


class Doctor(models.Model):
    """Veterinary Doctor/Veterinarian Model"""
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    license_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    clinic_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Dr. {self.name} - {self.license_number}"


class VeterinaryVisit(models.Model):
    """Veterinary Visit/Checkup Records"""
    VISIT_TYPE_CHOICES = (
        ('routine', 'Routine Checkup'),
        ('emergency', 'Emergency'),
        ('vaccination', 'Vaccination'),
        ('ai', 'Artificial Insemination'),
        ('pregnancy_check', 'Pregnancy Check'),
        ('treatment', 'Treatment'),
        ('other', 'Other'),
    )
    
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='veterinary_visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='visits')
    visit_date = models.DateField(default=timezone.now)
    visit_time = models.TimeField(default=timezone.now)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES, default='routine')
    reason_for_visit = models.TextField()
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment_given = models.TextField(blank=True, null=True)
    doctor_instructions = models.TextField(blank=True, null=True, help_text='Special instructions from doctor')
    next_visit_date = models.DateField(null=True, blank=True)
    visit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_visits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date', '-visit_time']
    
    def __str__(self):
        return f"{self.cow.cow_number} - {self.visit_type} - {self.visit_date}"


class Medicine(models.Model):
    """Medicine/Medication Records"""
    visit = models.ForeignKey(VeterinaryVisit, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, help_text='e.g., Twice daily, Once a day')
    duration = models.CharField(max_length=100, help_text='e.g., 5 days, 1 week')
    route = models.CharField(max_length=50, blank=True, null=True, help_text='e.g., Oral, Injection, Topical')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"


class ArtificialInsemination(models.Model):
    """Artificial Insemination (AI) Records"""
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='ai_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    ai_date = models.DateField(default=timezone.now)
    ai_time = models.TimeField(default=timezone.now)
    bull_breed = models.CharField(max_length=100, help_text='Breed of bull used for AI')
    bull_id = models.CharField(max_length=100, blank=True, null=True, help_text='Bull identification number')
    semen_source = models.CharField(max_length=200, blank=True, null=True)
    heat_detection_date = models.DateField(help_text='Date when cow was in heat')
    technician_name = models.CharField(max_length=100, blank=True, null=True)
    success_status = models.CharField(max_length=50, default='Pending', help_text='Pending/Confirmed/Failed')
    expected_calving_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-ai_date']
    
    def __str__(self):
        return f"{self.cow.cow_number} - AI on {self.ai_date}"


class Pregnancy(models.Model):
    """Pregnancy Tracking Records"""
    PREGNANCY_STATUS_CHOICES = (
        ('suspected', 'Suspected'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
        ('aborted', 'Aborted'),
        ('delivered', 'Delivered'),
    )
    
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='pregnancies')
    ai_record = models.ForeignKey(ArtificialInsemination, on_delete=models.SET_NULL, null=True, blank=True, related_name='pregnancy')
    confirmation_date = models.DateField(help_text='Date when pregnancy was confirmed')
    confirmed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    pregnancy_status = models.CharField(max_length=20, choices=PREGNANCY_STATUS_CHOICES, default='suspected')
    expected_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    pregnancy_duration = models.IntegerField(null=True, blank=True, help_text='Duration in days')
    calf_gender = models.CharField(max_length=10, blank=True, null=True, choices=(('male', 'Male'), ('female', 'Female')))
    calf_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Weight in kg')
    delivery_type = models.CharField(max_length=50, blank=True, null=True, help_text='Normal/C-Section/Assisted')
    complications = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_pregnancies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-confirmation_date']
        verbose_name_plural = 'Pregnancies'
    
    def __str__(self):
        return f"{self.cow.cow_number} - {self.pregnancy_status} - {self.expected_delivery_date}"


class Vaccination(models.Model):
    """Vaccination Records"""
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=200)
    disease_prevention = models.CharField(max_length=200, help_text='Disease this vaccine prevents')
    vaccination_date = models.DateField(default=timezone.now)
    next_due_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    administered_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    dosage = models.CharField(max_length=100)
    route = models.CharField(max_length=50, help_text='e.g., Subcutaneous, Intramuscular')
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-vaccination_date']
    
    def __str__(self):
        return f"{self.cow.cow_number} - {self.vaccine_name} - {self.vaccination_date}"
