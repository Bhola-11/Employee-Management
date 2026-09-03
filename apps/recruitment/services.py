from .models import JobRequisition, Candidate, JobApplication, RecruitmentStage, InterviewSchedule, JobOffer
from apps.audit.services import AuditService

class RecruitmentService:
    @staticmethod
    def get_pipeline_summary(organization):
        reqs = JobRequisition.objects.filter(organization=organization)
        total_open = reqs.filter(status='OPEN').count()
        total_candidates = Candidate.objects.filter(organization=organization).count()
        active_apps = JobApplication.objects.filter(requisition__organization=organization).exclude(status__in=['HIRED', 'REJECTED', 'WITHDRAWN']).count()
        hired_count = JobApplication.objects.filter(requisition__organization=organization, status='HIRED').count()
        return {
            'total_open_positions': total_open,
            'total_candidates': total_candidates,
            'active_applications': active_apps,
            'hired_count': hired_count
        }

    @staticmethod
    def advance_candidate_stage(application, next_stage, user):
        old_stage = application.current_stage.name if application.current_stage else 'None'
        application.current_stage = next_stage
        if next_stage.name.upper() == 'HIRED':
            application.status = 'HIRED'
        elif next_stage.name.upper() == 'REJECTED':
            application.status = 'REJECTED'
        else:
            application.status = 'INTERVIEWING'
        application.save()
        
        AuditService.log_activity(
            organization=application.requisition.organization,
            user=user,
            module='recruitment',
            action='UPDATE',
            obj=application,
            description=f"Moved candidate {application.candidate.full_name} from stage '{old_stage}' to '{next_stage.name}'"
        )
        return application
