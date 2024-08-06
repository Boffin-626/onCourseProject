from django.contrib import admin
from .models import User, Learner, ProgressReport, Parent, School, Teacher, ConceptGrasp, USSDRequest, WhatsAppRequest

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(ProgressReport)
admin.site.register(Parent)
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(ConceptGrasp)
admin.site.register(USSDRequest)
admin.site.register(WhatsAppRequest)