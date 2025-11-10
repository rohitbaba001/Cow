from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Worker, Task, Cow, Doctor, VeterinaryVisit, 
                     Medicine, ArtificialInsemination, Pregnancy, Vaccination)


class WorkerCreationForm(UserCreationForm):
    """Form for Admin to create workers"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    employee_id = forms.CharField(max_length=50, required=True)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'worker'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.address = self.cleaned_data.get('address', '')
        
        if commit:
            user.save()
            Worker.objects.create(
                user=user,
                employee_id=self.cleaned_data['employee_id'],
                date_of_joining=self.cleaned_data['date_of_joining']
            )
        return user


class TaskForm(forms.ModelForm):
    """Form for creating and assigning tasks"""
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'notes', 'deadline', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class CowForm(forms.ModelForm):
    """Form for adding/editing cows"""
    last_checkup = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Cow
        fields = ['cow_number', 'cow_name', 'breed', 'age', 'color', 
                  'identification_mark', 'health_status', 'last_checkup', 'notes', 'photo', 'is_active']
        widgets = {
            'identification_mark': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class DoctorForm(forms.ModelForm):
    """Form for adding/editing doctors"""
    class Meta:
        model = Doctor
        fields = ['name', 'qualification', 'specialization', 'license_number', 
                  'phone_number', 'email', 'clinic_name', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class VeterinaryVisitForm(forms.ModelForm):
    """Form for veterinary visits"""
    visit_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    visit_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    next_visit_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = VeterinaryVisit
        fields = ['cow', 'doctor', 'visit_date', 'visit_time', 'visit_type', 'reason_for_visit',
                  'symptoms', 'diagnosis', 'treatment_given', 'doctor_instructions', 
                  'next_visit_date', 'visit_cost', 'notes']
        widgets = {
            'reason_for_visit': forms.Textarea(attrs={'rows': 2}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment_given': forms.Textarea(attrs={'rows': 3}),
            'doctor_instructions': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class MedicineForm(forms.ModelForm):
    """Form for adding medicines"""
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'dosage', 'frequency', 'duration', 'route', 
                  'start_date', 'end_date', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2}),
        }


class ArtificialInseminationForm(forms.ModelForm):
    """Form for AI records"""
    ai_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    ai_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    heat_detection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expected_calving_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = ArtificialInsemination
        fields = ['cow', 'doctor', 'ai_date', 'ai_time', 'bull_breed', 'bull_id', 
                  'semen_source', 'heat_detection_date', 'technician_name', 
                  'success_status', 'expected_calving_date', 'cost', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class PregnancyForm(forms.ModelForm):
    """Form for pregnancy tracking"""
    confirmation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expected_delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    actual_delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Pregnancy
        fields = ['cow', 'ai_record', 'confirmation_date', 'confirmed_by', 'pregnancy_status',
                  'expected_delivery_date', 'actual_delivery_date', 'pregnancy_duration',
                  'calf_gender', 'calf_weight', 'delivery_type', 'complications', 'doctor_notes']
        widgets = {
            'complications': forms.Textarea(attrs={'rows': 3}),
            'doctor_notes': forms.Textarea(attrs={'rows': 3}),
        }


class VaccinationForm(forms.ModelForm):
    """Form for vaccination records"""
    vaccination_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    next_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Vaccination
        fields = ['cow', 'vaccine_name', 'disease_prevention', 'vaccination_date', 
                  'next_due_date', 'batch_number', 'administered_by', 'dosage', 'route', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class TaskUpdateForm(forms.ModelForm):
    """Form for workers to update task status"""
    class Meta:
        model = Task
        fields = ['status']
