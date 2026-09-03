from django.contrib import admin
from .models import JobRequisition, RecruitmentStage, Candidate, JobApplication, InterviewSchedule, InterviewFeedback, JobOffer

admin.site.register(JobRequisition)
admin.site.register(RecruitmentStage)
admin.site.register(Candidate)
admin.site.register(JobApplication)
admin.site.register(InterviewSchedule)
admin.site.register(InterviewFeedback)
admin.site.register(JobOffer)
