from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from.models import Doctor,Patient,Appointment,EHR,ApprovalRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from reg.models import CustomUser
from django.views.decorators.csrf import csrf_protect
@csrf_protect
@login_required

def index(request):
    return render(request, 'index.html')



def doctor_homepage(request):
    # Retrieve the currently logged-in user
    current_user = request.user
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If authenticated, retrieve the doctor associated with the current user
        try:
            doctor = Doctor.objects.get(id=current_user)
        except Doctor.DoesNotExist:
            # If the doctor does not exist, set doctor to None
            doctor = None
    else:
        # If the user is not authenticated, set doctor to None
        doctor = None
    return render(request, 'doctor_homepage.html', {'doctor': doctor})


def doctor_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specification = request.POST.get('specification')
        location = request.POST.get('location')
        contact_information = request.POST.get('contact_information')
        profile_picture = request.FILES.get('profile_picture')   
        email = request.POST.get('email')  # Retrieve email from the request   
        
        # Retrieve the CustomUser instance of the logged-in user
        custom_user = request.user
        username = request.user.username 
        
        if custom_user is None:
            return HttpResponse("User is not authenticated")
        
        try:
            # Check if the doctor already exists
            doctor = Doctor.objects.get(user_id=custom_user.id)
            # If the doctor already exists, update its attributes
            doctor.name = username
            doctor.specification = specification
            doctor.location = location
            doctor.contact_information = contact_information
            doctor.email = email 
            if profile_picture:
                doctor.profile_picture = profile_picture
            doctor.save()
        except Doctor.DoesNotExist:
            # If the doctor doesn't exist, create a new one
            doctor = Doctor.objects.create(id=custom_user,user_id=custom_user.id, name=username, specification=specification, location=location, contact_information=contact_information, profile_picture=profile_picture, email=email)
        return redirect('doctor_homepage')  # Redirect to the homepage after creating/updating the doctor
    
    # Get the current doctor profile details
    try:
        current_doctor = Doctor.objects.get(user_id=request.user.id)
    except Doctor.DoesNotExist:
        current_doctor = None
    
    return render(request, 'doctor_profile.html', {'current_doctor': current_doctor})


def search_patient(request):
    if request.method == 'GET':
        query = request.GET.get('username', '')
        if query:
            patients = Patient.objects.filter(id__username__icontains=query)
            return render(request, 'search_patient.html', {'patients': patients, 'query': query})
    return render(request, 'search_patient.html', {'patients': None, 'query': None})
        

def patient_homepage(request):
    # Retrieve the currently logged-in user
    current_user = request.user
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If authenticated, retrieve the patient associated with the current user
        try:
            patient = Patient.objects.get(id=current_user)
        except Patient.DoesNotExist:
            # If the patient does not exist, set patient to None
            patient = None
    else:
        # If the user is not authenticated, set patient to None
        patient = None
    return render(request, 'patient_homepage.html', {'patient': patient})



def search_doctor(request):
    if request.method == 'GET':
        query = request.GET.get('username', '')
        if query:
            doctors = Doctor.objects.filter(id__username__icontains=query)
            return render(request, 'search_doctor.html', {'doctors': doctors, 'query': query})
        else:
            doctors = Doctor.objects.all()  # Retrieve all doctors
            return render(request, 'search_doctor.html', {'doctors': doctors, 'query': None})
    return render(request, 'search_doctor.html', {'doctors': None, 'query': None})


def patient_profile(request):
    # Initialize current profile values to None
    current_values = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        contact_information = request.POST.get('contact_information')
        profile_picture = request.FILES.get('profile_picture')  
        email = request.POST.get('email')     
        # Retrieve the CustomUser instance of the logged-in user
        custom_user = request.user
        username = request.user.username  
        if custom_user is None:
            return HttpResponse("User is not authenticated") 
        # Check if the patient already exists
        try:
            patient = Patient.objects.get(id=custom_user)
            # If the patient already exists, update its attributes
            patient.name = username
            patient.dob = dob
            patient.gender = gender
            patient.location = location
            patient.contact_information = contact_information
            patient.email = email 
            if profile_picture:
                patient.profile_picture = profile_picture
            patient.save()
        except Patient.DoesNotExist:
            # If the patient doesn't exist, create a new one
            patient = Patient.objects.create(id=custom_user,user_id=custom_user.id, name=username, dob=dob, gender=gender, location=location, contact_information=contact_information, profile_picture=profile_picture,email=email) 
        return redirect('patient_homepage')  # Redirect to the homepage after creating/updating the patient profile
    else:
        # If it's a GET request, try to retrieve the current patient profile
        try:
            patient = Patient.objects.get(id=request.user)
            # If the patient exists, populate the current values
            current_values = {
                'name': patient.name,
                'dob': patient.dob,
                'gender': patient.gender,
                'location': patient.location,
                'contact_information': patient.contact_information,
                'email': patient.email,
                'profile_picture': patient.profile_picture,
                # Add more fields as needed
            }
        except Patient.DoesNotExist:
            pass  # If the patient doesn't exist, current_values will remain None
            
    return render(request, 'patient_profile.html', {'current_values': current_values})



def patient_appointment(request):
    if request.method == 'POST':
        if 'doctor_id' in request.POST:  # Booking appointment
            patient = Patient.objects.get(user_id=request.user.id)
            doctor_id = request.POST.get('doctor_id')
            doctor = Doctor.objects.get(user_id=doctor_id)
            # Check if there's an existing appointment for the same patient and doctor
            existing_appointment = Appointment.objects.filter(patient=patient, doctor=doctor).exists()
            if existing_appointment:
                return JsonResponse({'message': 'Appointment already exists for this patient and doctor.'}, status=400)
            else:
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    
                    status='Pending'
                )
                return redirect('patient_appointment')

        elif 'action' in request.POST and request.POST.get('action') == 'cancel':  # Cancelling appointment
            appointment_id = request.POST.get('appointment_id')
            Appointment.objects.filter(id=appointment_id).delete()
            return redirect('patient_appointment')

    doctors = Doctor.objects.all()
    patient = request.user.patient
    appointments = patient.appointment_set.all()

    return render(request, 'patient_appointment.html', {'doctors': doctors, 'appointments': appointments})


def doctor_appointment(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        appointment_id = request.POST.get('appointment_id')

        if action == 'cancel':
            Appointment.objects.filter(id=appointment_id).delete()
            return redirect('doctor_homepage')
        elif action == 'accept':
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_datetime = request.POST.get('appointment_datetime')
            appointment.date = appointment_datetime.split('T')[0]  # Extract date
            appointment.time = appointment_datetime.split('T')[1]  # Extract time
            appointment.status = 'Accepted'
            appointment.save()
            return redirect('doctor_homepage')
        elif action == 'reject':
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = 'Rejected'
            appointment.save()
            return redirect('doctor_homepage')

    doctor = Doctor.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctor_appointment.html', {'appointments': appointments})


def view_ehr(request):
    # Fetch all EHR records for the current patient
    ehrs = EHR.objects.filter(patient=request.user.patient)
    return render(request, 'view_ehr.html', {'ehrs': ehrs})

def edit_ehr(request):
    patient = request.user.patient
    # Get all EHRs for the current patient
    patient_ehrs = EHR.objects.filter(patient=patient)

    if request.method == 'POST':
        # Process the form submission
        ehr_id = request.POST.get('ehr_id')
        if ehr_id:
            ehr = EHR.objects.get(pk=ehr_id)
        else:
            # Create a new EHR if no ID is provided
            ehr = EHR(patient=patient)
        ehr.symptoms = request.POST.get('symptoms', '')
        ehr.diagnosis = request.POST.get('diagnosis', '')
        ehr.medications = request.POST.get('medications', '')
        ehr.allergies = request.POST.get('allergies', '')
        ehr.personal_history = request.POST.get('personal_history', '')
        ehr.family_history = request.POST.get('family_history', '')
        ehr.drug_history = request.POST.get('drug_history', '')
        ehr.vital_signs = request.POST.get('vital_signs', '')
        ehr.notes = request.POST.get('notes', '')
        ehr.xray_image = request.FILES.get('xray_image')
        ehr.lab_result_image = request.FILES.get('lab_result_image')
        ehr.save()
        return redirect('view_ehr')

    return render(request, 'edit_ehr.html', {'patient_ehrs': patient_ehrs})

from django.http import request






def patient_ehr(request):
    return render(request, 'patient_ehr.html')


def cancer_detection(request):
    return render(request, 'cancer_detection.html')

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from django.shortcuts import get_object_or_404


def doctor_ehr(request):
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'cancel':
            request_id = request.POST.get('request_id')
            approval_request = get_object_or_404(ApprovalRequest, id=request_id)
            approval_request.delete()
            messages.success(request, "Approval request cancelled successfully.")
            return redirect('doctor_ehr')

    if request.method == 'POST':
        # Handling approval request submission
        if 'patient_id' in request.POST:
            doctor = request.user.doctor
            patient_id = request.POST.get('patient_id')
            patient = get_object_or_404(Patient, id=patient_id)
            existing_request = ApprovalRequest.objects.filter(doctor=doctor, patient=patient, status='pending').exists()
            if existing_request:
                messages.warning(request, f"Approval request already pending for {patient.name}.")
            else:
                ApprovalRequest.objects.create(doctor=doctor, patient=patient, status='pending')
                messages.success(request, f"Approval request sent to {patient.name}.")
            return redirect('doctor_ehr')
        
        # Handling cancellation of approval request
        elif 'action' in request.POST and request.POST.get('action') == 'cancel_request':
            request_id = request.POST.get('request_id')
            ApprovalRequest.objects.filter(id=request_id).delete()
            messages.success(request, "Approval request cancelled successfully.")
            return redirect('doctor_homepage')

    search_query = request.GET.get('search_query', '')
    search_results = None
    pending_requests = []
    approved_patients  = []
    
    # Searching patients by name or medical record number

    if search_query:
        search_results = Patient.objects.filter(name__icontains=search_query)

    if request.user.is_authenticated and hasattr(request.user, 'doctor'):
        current_doctor = request.user.doctor
        # Retrieve pending approval requests for the current doctor
        pending_requests = ApprovalRequest.objects.filter(doctor=current_doctor, status='pending')
        # Retrieve approved patients for the current doctor
        approved_patients = Patient.objects.filter(approvalrequest__doctor=current_doctor, approvalrequest__status='approved')

    return render(request, 'doctor_ehr.html', {'search_query': search_query, 'search_results': search_results, 'pending_requests': pending_requests, 'approved_patients': approved_patients})


from django.http import HttpResponseForbidden, Http404


def doctor_edit(request, patient_id):
    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=patient_id)
    # Get all EHRs for the current patient
    doctor_ehrs = EHR.objects.filter(doctor=doctor)
    
    if request.method == 'POST':
        # Process the form submission
        ehr_id = request.POST.get('ehr_id')
        if ehr_id:
            ehr = get_object_or_404(EHR, pk=ehr_id)
        else:
            # Create a new EHR if no ID is provided
            ehr = EHR(patient=patient, doctor=doctor)
        
        # Assign values to the EHR fields
        ehr.symptoms = request.POST.get('symptoms', '')
        ehr.diagnosis = request.POST.get('diagnosis', '')
        ehr.medications = request.POST.get('medications', '')
        ehr.allergies = request.POST.get('allergies', '')
        ehr.personal_history = request.POST.get('personal_history', '')
        ehr.family_history = request.POST.get('family_history', '')
        ehr.drug_history = request.POST.get('drug_history', '')
        ehr.vital_signs = request.POST.get('vital_signs', '')
        ehr.notes = request.POST.get('notes', '')
        ehr.xray_image = request.FILES.get('xray_image')
        ehr.lab_result_image = request.FILES.get('lab_result_image')
        # Save the EHR object
        ehr.save()
        
        return redirect('doctor_ehr')

    return render(request, 'doctor_edit.html', {'doctor_ehrs': doctor_ehrs, 'patient': patient})
    

def pending_requests(request):
    if request.user.is_authenticated and hasattr(request.user, 'patient'):
        patient = request.user.patient
        pending_requests = ApprovalRequest.objects.filter(patient=patient, status='pending')
        accepted_request = ApprovalRequest.objects.filter(patient=patient, status__in=['approved', 'rejected']).first()
        
        if request.method == 'POST':
            action = request.POST.get('action')
            request_id = request.POST.get('request_id')
            
            if action and request_id:
                if action == 'cancel':
                    approval_request = get_object_or_404(ApprovalRequest, id=request_id, patient=patient)
                    approval_request.delete()
                    messages.success(request, 'Request cancelled successfully')
                    return redirect('pending_requests')  # Redirect back to the pending requests page after cancellation
                else:
                    approval_request = get_object_or_404(ApprovalRequest, id=request_id, patient=patient)
                    if action == 'accept':
                        approval_request.approve_request()
                        messages.success(request, 'Request accepted successfully')
                    elif action == 'reject':
                        approval_request.deny_request()
                        messages.success(request, 'Request rejected successfully')
                return redirect('pending_requests')
        
        return render(request, 'pending_requests.html', {'pending_requests': pending_requests, 'accepted_request': accepted_request})
    
    else:
        return redirect('login')
    


def doctor_view(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ehrs = EHR.objects.filter(patient=patient)
    return render(request,'doctor_view.html', {'ehrs': ehrs})