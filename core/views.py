from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import (User, Worker, Task, Cow, Doctor, VeterinaryVisit, 
                     Medicine, ArtificialInsemination, Pregnancy, Vaccination)
from .forms import WorkerCreationForm, TaskForm, CowForm, TaskUpdateForm


def login_view(request):
    """Login page with language selection"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        language = request.POST.get('language', 'en')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['language'] = language
            messages.success(request, 'Login successful!' if language == 'en' else 'लॉगिन यशस्वी!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!' if language == 'en' else 'अवैध प्रमाणपत्रे!')
    
    language = request.GET.get('lang', 'en')
    
    # Render with cache control headers
    response = render(request, 'login.html', {'language': language})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
def logout_view(request):
    """Logout user"""
    # Clear session completely
    request.session.flush()
    logout(request)
    
    # Create response with cache control
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    messages.success(request, 'Logged out successfully!')
    return response


@login_required
def dashboard(request):
    """Main dashboard - different views for admin and worker"""
    language = request.session.get('language', 'en')
    
    if request.user.user_type == 'admin':
        # Admin Dashboard
        total_workers = Worker.objects.filter(is_active=True).count()
        total_tasks = Task.objects.all().count()
        pending_tasks = Task.objects.filter(status='pending').count()
        total_cows = Cow.objects.filter(is_active=True).count()
        
        recent_tasks = Task.objects.all()[:5]
        recent_cows = Cow.objects.filter(is_active=True)[:5]
        
        context = {
            'language': language,
            'total_workers': total_workers,
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'total_cows': total_cows,
            'recent_tasks': recent_tasks,
            'recent_cows': recent_cows,
        }
        return render(request, 'admin_dashboard.html', context)
    else:
        # Worker Dashboard
        try:
            worker = request.user.worker_profile
            my_tasks = Task.objects.filter(assigned_to=worker)
            pending_tasks = my_tasks.filter(status='pending').count()
            in_progress_tasks = my_tasks.filter(status='in_progress').count()
            completed_tasks = my_tasks.filter(status='completed').count()
            
            context = {
                'language': language,
                'my_tasks': my_tasks[:10],
                'pending_tasks': pending_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completed_tasks': completed_tasks,
            }
            return render(request, 'worker_dashboard.html', context)
        except:
            messages.error(request, 'Worker profile not found!')
            return redirect('login')


# Worker Management Views
@login_required
def worker_list(request):
    """List all workers (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    workers = Worker.objects.select_related('user').all()
    
    return render(request, 'worker_list.html', {'workers': workers, 'language': language})


@login_required
def worker_create(request):
    """Create new worker (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    
    if request.method == 'POST':
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Worker created successfully!' if language == 'en' else 'कामगार यशस्वीरित्या तयार केला!')
            return redirect('worker_list')
    else:
        form = WorkerCreationForm()
    
    return render(request, 'worker_form.html', {'form': form, 'language': language})


@login_required
def worker_delete(request, pk):
    """Delete worker (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    worker = get_object_or_404(Worker, pk=pk)
    
    if request.method == 'POST':
        worker.is_active = False
        worker.save()
        messages.success(request, 'Worker deactivated!' if language == 'en' else 'कामगार निष्क्रिय केला!')
        return redirect('worker_list')
    
    return render(request, 'worker_confirm_delete.html', {'worker': worker, 'language': language})


# Task Management Views
@login_required
def task_list(request):
    """List all tasks"""
    language = request.session.get('language', 'en')
    
    if request.user.user_type == 'admin':
        tasks = Task.objects.select_related('assigned_to__user', 'assigned_by').all()
    else:
        worker = request.user.worker_profile
        tasks = Task.objects.filter(assigned_to=worker)
    
    return render(request, 'task_list.html', {'tasks': tasks, 'language': language})


@login_required
def task_create(request):
    """Create new task (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            messages.success(request, 'Task assigned successfully!' if language == 'en' else 'कार्य यशस्वीरित्या नियुक्त केले!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'task_form.html', {'form': form, 'language': language})


@login_required
def task_detail(request, pk):
    """View task details"""
    language = request.session.get('language', 'en')
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'admin' and task.assigned_to.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    return render(request, 'task_detail.html', {'task': task, 'language': language})


@login_required
def task_update(request, pk):
    """Update task (Admin can edit all, Worker can only update status)"""
    language = request.session.get('language', 'en')
    task = get_object_or_404(Task, pk=pk)
    
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task updated!' if language == 'en' else 'कार्य अद्यतनित!')
                return redirect('task_detail', pk=pk)
        else:
            form = TaskForm(instance=task)
        return render(request, 'task_form.html', {'form': form, 'task': task, 'language': language})
    else:
        # Worker can only update status
        if task.assigned_to.user != request.user:
            messages.error(request, 'Access denied!')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = TaskUpdateForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.status == 'completed':
                    task.completed_at = timezone.now()
                task.save()
                messages.success(request, 'Status updated!' if language == 'en' else 'स्थिती अद्यतनित!')
                return redirect('task_detail', pk=pk)
        else:
            form = TaskUpdateForm(instance=task)
        return render(request, 'task_status_form.html', {'form': form, 'task': task, 'language': language})


@login_required
def task_delete(request, pk):
    """Delete task (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!' if language == 'en' else 'कार्य हटवले!')
        return redirect('task_list')
    
    return render(request, 'task_confirm_delete.html', {'task': task, 'language': language})


# Cow/Veterinary Management Views
@login_required
def cow_list(request):
    """List all cows"""
    language = request.session.get('language', 'en')
    cows = Cow.objects.filter(is_active=True)
    
    return render(request, 'cow_list.html', {'cows': cows, 'language': language})


@login_required
def cow_create(request):
    """Add new cow (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    
    if request.method == 'POST':
        form = CowForm(request.POST, request.FILES)
        if form.is_valid():
            cow = form.save(commit=False)
            cow.added_by = request.user
            cow.save()
            messages.success(request, 'Cow added successfully!' if language == 'en' else 'गाय यशस्वीरित्या जोडली!')
            return redirect('cow_list')
    else:
        form = CowForm()
    
    return render(request, 'cow_form.html', {'form': form, 'language': language})


@login_required
def cow_detail(request, pk):
    """View cow details"""
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=pk)
    veterinary_visits = cow.veterinary_visits.all()
    ai_records = cow.ai_records.all()
    pregnancies = cow.pregnancies.all()
    vaccinations = cow.vaccinations.all()
    
    return render(request, 'cow_detail.html', {
        'cow': cow,
        'veterinary_visits': veterinary_visits,
        'ai_records': ai_records,
        'pregnancies': pregnancies,
        'vaccinations': vaccinations,
        'language': language
    })


@login_required
def cow_update(request, pk):
    """Update cow details (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=pk)
    
    if request.method == 'POST':
        form = CowForm(request.POST, request.FILES, instance=cow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cow updated!' if language == 'en' else 'गाय अद्यतनित!')
            return redirect('cow_detail', pk=pk)
    else:
        form = CowForm(instance=cow)
    
    return render(request, 'cow_form.html', {'form': form, 'cow': cow, 'language': language})


@login_required
def cow_delete(request, pk):
    """Delete cow (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard')
    
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=pk)
    
    if request.method == 'POST':
        cow.is_active = False
        cow.save()
        messages.success(request, 'Cow deactivated!' if language == 'en' else 'गाय निष्क्रिय केली!')
        return redirect('cow_list')
    
    return render(request, 'cow_confirm_delete.html', {'cow': cow, 'language': language})


def change_language(request):
    """Change language preference"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


# ==================== VETERINARY SYSTEM VIEWS ====================

from .forms import (DoctorForm, VeterinaryVisitForm, MedicineForm, 
                    ArtificialInseminationForm, PregnancyForm, VaccinationForm)

# Doctor Management
@login_required
def doctor_list(request):
    """List all doctors"""
    language = request.session.get('language', 'en')
    doctors = Doctor.objects.filter(is_active=True)
    
    return render(request, 'veterinary/doctor_list.html', {
        'doctors': doctors,
        'language': language
    })


@login_required
def doctor_create(request):
    """Add new doctor (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!' if request.session.get('language') == 'en' else 'प्रवेश नाकारला!')
        return redirect('doctor_list')
    
    language = request.session.get('language', 'en')
    
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.added_by = request.user
            doctor.save()
            messages.success(request, 'Doctor added successfully!' if language == 'en' else 'डॉक्टर यशस्वीरित्या जोडले!')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    
    return render(request, 'veterinary/doctor_form.html', {'form': form, 'language': language})


@login_required
def doctor_update(request, pk):
    """Update doctor details (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!' if request.session.get('language') == 'en' else 'प्रवेश नाकारला!')
        return redirect('doctor_list')
    
    language = request.session.get('language', 'en')
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated!' if language == 'en' else 'डॉक्टर अपडेट केले!')
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'veterinary/doctor_form.html', {'form': form, 'doctor': doctor, 'language': language})


# Veterinary Visit Management
@login_required
def visit_create(request, cow_id):
    """Add veterinary visit"""
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=cow_id)
    
    if request.method == 'POST':
        form = VeterinaryVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.recorded_by = request.user
            visit.save()
            
            # Update cow's last checkup
            cow.last_checkup = visit.visit_date
            cow.save()
            
            messages.success(request, 'Visit recorded!' if language == 'en' else 'भेट नोंदवली!')
            return redirect('cow_detail', pk=cow_id)
    else:
        form = VeterinaryVisitForm(initial={'cow': cow})
    
    return render(request, 'veterinary/visit_form.html', {'form': form, 'cow': cow, 'language': language})


@login_required
def visit_detail(request, pk):
    """View visit details"""
    language = request.session.get('language', 'en')
    visit = get_object_or_404(VeterinaryVisit, pk=pk)
    medicines = visit.medicines.all()
    
    return render(request, 'veterinary/visit_detail.html', {
        'visit': visit,
        'medicines': medicines,
        'language': language
    })


# Medicine Management
@login_required
def medicine_create(request, visit_id):
    """Add medicine to a visit"""
    language = request.session.get('language', 'en')
    visit = get_object_or_404(VeterinaryVisit, pk=visit_id)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.visit = visit
            medicine.save()
            messages.success(request, 'Medicine added!' if language == 'en' else 'औषध जोडले!')
            return redirect('visit_detail', pk=visit_id)
    else:
        form = MedicineForm()
    
    return render(request, 'veterinary/medicine_form.html', {'form': form, 'visit': visit, 'language': language})


# Artificial Insemination Management
@login_required
def ai_list(request):
    """List all AI records"""
    language = request.session.get('language', 'en')
    ai_records = ArtificialInsemination.objects.all().order_by('-ai_date')
    
    return render(request, 'veterinary/ai_list.html', {
        'ai_records': ai_records,
        'language': language
    })


@login_required
def ai_create(request, cow_id=None):
    """Record AI procedure"""
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=cow_id) if cow_id else None
    
    if request.method == 'POST':
        form = ArtificialInseminationForm(request.POST)
        if form.is_valid():
            ai_record = form.save(commit=False)
            ai_record.recorded_by = request.user
            ai_record.save()
            messages.success(request, 'AI record added!' if language == 'en' else 'कृत्रिम रेतन नोंद जोडली!')
            return redirect('ai_list')
    else:
        initial = {'cow': cow} if cow else {}
        form = ArtificialInseminationForm(initial=initial)
    
    return render(request, 'veterinary/ai_form.html', {'form': form, 'cow': cow, 'language': language})


@login_required
def ai_detail(request, pk):
    """View AI record details"""
    language = request.session.get('language', 'en')
    ai_record = get_object_or_404(ArtificialInsemination, pk=pk)
    pregnancy = ai_record.pregnancy.first() if hasattr(ai_record, 'pregnancy') else None
    
    return render(request, 'veterinary/ai_detail.html', {
        'ai_record': ai_record,
        'pregnancy': pregnancy,
        'language': language
    })


# Pregnancy Management
@login_required
def pregnancy_list(request):
    """List all pregnancies"""
    language = request.session.get('language', 'en')
    pregnancies = Pregnancy.objects.all().order_by('-confirmation_date')
    
    return render(request, 'veterinary/pregnancy_list.html', {
        'pregnancies': pregnancies,
        'language': language
    })


@login_required
def pregnancy_create(request, cow_id=None):
    """Record pregnancy"""
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=cow_id) if cow_id else None
    
    if request.method == 'POST':
        form = PregnancyForm(request.POST)
        if form.is_valid():
            pregnancy = form.save(commit=False)
            pregnancy.recorded_by = request.user
            pregnancy.save()
            messages.success(request, 'Pregnancy recorded!' if language == 'en' else 'गर्भधारणा नोंदवली!')
            return redirect('pregnancy_list')
    else:
        initial = {'cow': cow} if cow else {}
        form = PregnancyForm(initial=initial)
    
    return render(request, 'veterinary/pregnancy_form.html', {'form': form, 'cow': cow, 'language': language})


@login_required
def pregnancy_update(request, pk):
    """Update pregnancy details"""
    language = request.session.get('language', 'en')
    pregnancy = get_object_or_404(Pregnancy, pk=pk)
    
    if request.method == 'POST':
        form = PregnancyForm(request.POST, instance=pregnancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pregnancy updated!' if language == 'en' else 'गर्भधारणा अपडेट केली!')
            return redirect('pregnancy_list')
    else:
        form = PregnancyForm(instance=pregnancy)
    
    return render(request, 'veterinary/pregnancy_form.html', {'form': form, 'pregnancy': pregnancy, 'language': language})


# Vaccination Management
@login_required
def vaccination_list(request):
    """List all vaccinations"""
    language = request.session.get('language', 'en')
    vaccinations = Vaccination.objects.all().order_by('-vaccination_date')
    
    return render(request, 'veterinary/vaccination_list.html', {
        'vaccinations': vaccinations,
        'language': language
    })


@login_required
def vaccination_create(request, cow_id=None):
    """Record vaccination"""
    language = request.session.get('language', 'en')
    cow = get_object_or_404(Cow, pk=cow_id) if cow_id else None
    
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.recorded_by = request.user
            vaccination.save()
            messages.success(request, 'Vaccination recorded!' if language == 'en' else 'लसीकरण नोंदवले!')
            return redirect('vaccination_list')
    else:
        initial = {'cow': cow} if cow else {}
        form = VaccinationForm(initial=initial)
    
    return render(request, 'veterinary/vaccination_form.html', {'form': form, 'cow': cow, 'language': language})


@login_required
def veterinary_dashboard(request):
    """Veterinary dashboard with overview"""
    language = request.session.get('language', 'en')
    
    # Get statistics
    total_doctors = Doctor.objects.filter(is_active=True).count()
    recent_visits = VeterinaryVisit.objects.all().order_by('-visit_date')[:5]
    pending_ai = ArtificialInsemination.objects.filter(success_status='Pending').count()
    active_pregnancies = Pregnancy.objects.filter(pregnancy_status='confirmed').count()
    upcoming_vaccinations = Vaccination.objects.filter(
        next_due_date__gte=timezone.now().date()
    ).order_by('next_due_date')[:5]
    
    return render(request, 'veterinary/dashboard.html', {
        'total_doctors': total_doctors,
        'recent_visits': recent_visits,
        'pending_ai': pending_ai,
        'active_pregnancies': active_pregnancies,
        'upcoming_vaccinations': upcoming_vaccinations,
        'language': language
    })
