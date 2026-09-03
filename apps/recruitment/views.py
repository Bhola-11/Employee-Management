from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import JobRequisition, Candidate, JobApplication, RecruitmentStage, InterviewSchedule, InterviewFeedback, JobOffer
from .forms import JobRequisitionForm, CandidateForm, InterviewScheduleForm, InterviewFeedbackForm, JobOfferForm
from .services import RecruitmentService

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE', 'RECRUITER')
def recruitment_dashboard_view(request):
    org = request.tenant_org
    metrics = RecruitmentService.get_pipeline_summary(org)
    recent_requisitions = JobRequisition.objects.filter(organization=org)[:6]
    recent_candidates = Candidate.objects.filter(organization=org)[:8]
    upcoming_interviews = InterviewSchedule.objects.filter(application__requisition__organization=org, status='SCHEDULED')[:5]
    
    return render(request, 'recruitment/dashboard.html', {
        'metrics': metrics,
        'requisitions': recent_requisitions,
        'candidates': recent_candidates,
        'upcoming_interviews': upcoming_interviews
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE', 'RECRUITER')
def requisition_list_view(request):
    org = request.tenant_org
    requisitions = JobRequisition.objects.filter(organization=org)
    return render(request, 'recruitment/requisition_list.html', {'requisitions': requisitions})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'RECRUITER')
def requisition_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = JobRequisitionForm(request.POST, organization=org)
        if form.is_valid():
            req = form.save(commit=False)
            req.organization = org
            req.save()
            messages.success(request, f"Requisition '{req.title}' created successfully.")
            return redirect('recruitment:requisition_detail', req.id)
    else:
        form = JobRequisitionForm(organization=org)
    return render(request, 'recruitment/requisition_form.html', {'form': form, 'title': 'Create Job Requisition'})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE', 'RECRUITER')
def requisition_detail_view(request, requisition_id):
    org = request.tenant_org
    req = get_object_or_404(JobRequisition, id=requisition_id, organization=org)
    stages = RecruitmentStage.objects.filter(organization=org).order_by('order')
    applications = req.applications.select_related('candidate', 'current_stage').all()
    
    pipeline = {}
    for st in stages:
        pipeline[st] = [app for app in applications if app.current_stage_id == st.id]
        
    return render(request, 'recruitment/requisition_detail.html', {
        'requisition': req,
        'stages': stages,
        'pipeline': pipeline,
        'applications': applications
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE', 'RECRUITER')
def candidate_list_view(request):
    org = request.tenant_org
    candidates = Candidate.objects.filter(organization=org)
    return render(request, 'recruitment/candidate_list.html', {'candidates': candidates})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'RECRUITER')
def candidate_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            cand = form.save(commit=False)
            cand.organization = org
            cand.save()
            messages.success(request, f"Candidate {cand.full_name} added to talent pool.")
            return redirect('recruitment:candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'recruitment/candidate_form.html', {'form': form, 'title': 'Add Candidate Profile'})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE', 'RECRUITER')
def candidate_detail_view(request, candidate_id):
    org = request.tenant_org
    cand = get_object_or_404(Candidate, id=candidate_id, organization=org)
    apps = cand.applications.select_related('requisition', 'current_stage').all()
    return render(request, 'recruitment/candidate_detail.html', {'candidate': cand, 'applications': apps})
