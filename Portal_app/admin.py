from django.contrib import admin
from .models import *

admin.site.register(UserMaster)
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(JobDetails)
admin.site.register(application) 

