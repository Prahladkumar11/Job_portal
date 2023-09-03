from django.shortcuts import render,redirect
from .models import *
from django.contrib import sessions
from random import randint
from django.contrib.auth import logout
from django.db.models import Q


def IndexPage(request):
    
    company=Company.objects.all()
    candidate=Candidate.objects.all()
    applications=application.objects.all()
    
    
    
    joblist = JobDetails.objects.filter(is_active=True).order_by('-id') 
    paginator = Paginator(joblist, 4)  
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)
    
    parttime = JobDetails.objects.filter(JobType='Part Time',is_active=True)
    fulltime = JobDetails.objects.filter(JobType='Full Time',is_active=True)
    
    
    context = {
        'joblist': page_jobs,
        "job":joblist,
        'company': company,
        "Candidate": candidate,
        'parttime': parttime,
        'fulltime': fulltime ,
        "application": applications
    }
   
        
    return render(request, 'index.html',context)
     


def SignUp(request):
    return render(request, 'signup.html')


def RegisterUser(request):
# Define valid choices for the 'role' field
    VALID_ROLES = ['Candidate', 'Company']


    if request.method == 'POST':
        role = request.POST.get('role')
        if role not in VALID_ROLES:
            return render(request, 'signup.html', {'msg': 'Invalid role'})

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        companyname=request.POST.get('companyname')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Check if the email already exists
        if UserMaster.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'msg': 'Email already exists'})

        if password == cpassword:
            # Generate the opt
            otp = randint(100000, 999999)

            # Create a new user with hashed password
            user = UserMaster.objects.create(email=email, role=role,otp=otp, password=password)

            if role == 'Candidate':
                # Create a new candidate profile
                Candidate.objects.create(userid=user, firstname=firstname, lastname=lastname)
            elif role == 'Company':
                # Create a new company profile
                Company.objects.create(userid=user, firstname=firstname, lastname=lastname,CompanyName=companyname)

            return render(request, 'otp.html', {'otp': otp,'email': email,'password': password })
        else:
            return render(request, 'signup.html', {'msg': 'Passwords do not match'})

    return render(request, 'signup.html')


def OtpPage(request):
    Email=request.POST.get('email')
    opt_1=request.POST.get('opt')
    user=UserMaster.objects.get(email=Email)
    if opt_1==str(user.otp):
        LoginUser(request)
        return redirect('index')
        # return render(request, 'login.html', {'msg': "Signup Successfull"})
    else:
        return render(request, 'otp.html', {'msg': "Invalid OTP"})

def LoginPage(request):
    logout(request)
    return render(request, 'login.html')

def LoginUser(request):
    email = request.POST['email'].lower()
 
    password = request.POST['password']
    
    try:
        user = UserMaster.objects.get(email=email)
      
        if user:
            if user.password == password and user.role == 'Candidate':
                cand = Candidate.objects.get(userid=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = cand.firstname
                request.session['lastname'] = cand.lastname
                request.session['email'] = user.email
                
                return redirect('index')
            
            elif user.password == password and user.role == 'Company':
                cand = Company.objects.get(userid=user)
                request.session['method']=request.method
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = cand.firstname
                request.session['lastname'] = cand.lastname
                request.session['email'] = user.email
                request.session['CompanyName'] = cand.CompanyName
                

                return redirect('company')  # Add this line to return HttpResponse for Company authentication
            
            else:
                return render(request, 'login.html', {'msg': 'Invalid password'})
        
    except UserMaster.DoesNotExist as e: 
        return render(request, 'login.html', {'msg': 'Invalid User '})
         
def ProfilePage(request):
    try:
        try:
            user_id = request.session['id']
            if request.session['role']=='Candidate':
                user_data = Candidate.objects.get(userid=user_id)
                return render(request, 'profile.html', {'user_data': user_data})
            else:
                user_data = Company.objects.get(userid=user_id)
                return render(request, 'companyProfile.html', {'user_data': user_data})
        except:
            logout(request)
            return render(request, 'login.html', {'msg': 'Please Login'})
        
        
    except Candidate.DoesNotExist:
        
        return render(request, 'profile.html')
        
        

    # Pass the user_data to the template and render the profile.html
    

def UpdateCandidateProfile(request):
    if request.method == 'POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        address=request.POST.get('address')
        state=request.POST.get('state')
        city=request.POST.get('city')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        education=request.POST.get('education')
        website=request.POST.get('website')
        contact=request.POST.get('contact')
        
        try:
            udata = Candidate.objects.get(userid=request.session['id'])
            
            
            udata.firstname = firstname
            udata.lastname = lastname
            udata.address=address
            udata.state=state
            udata.city = city
            udata.gender = gender
            udata.dob= dob
            udata.education = education
            udata.website = website
            udata.contact = contact
            
            
            udata.save()

        # Redirect back to the same page (home.html) after processing the image upload
            return redirect('profile')
        except:
            logout(request)
            return render(request, 'login.html', {'msg': 'Please Login first with candidate accout'})

def UpdatePics(request):
    if request.method == 'POST':
        pics=request.FILES.get('profile_pics')
        print(pics,"@@@@@@")
        
        if pics :
            try:
                user_id = request.session['id']
                user_data = Candidate.objects.get(userid=user_id)
                first_name = user_data.firstname
                last_name = user_data.lastname
                if user_data.profile_pic:
                    oldFilename=str(user_data.profile_pic)
                    filena,ext=oldFilename.rsplit('-',1)
                    
                    count,ext=ext.rsplit('.',1)
                    try:
                        count,_=count.rsplit('_',1)
                    except  :  
                        pass
                    if int(count)<1:
                        count=1
                    else:
                        count = int(count)+1
                else: 
                    count=1
        
                # Generate a filename using first name and last name
                filename = f"{first_name}{last_name}({request.session['email']})/img-{count}.jpg"  # You can adjust the file extension as needed
                
                # Save the picture with the generated filename
                user_data.profile_pic.save(filename, pics)
                user_data.save()
                
                return redirect('profile')
                
            except Candidate.DoesNotExist:
                pass
                
        return redirect('profile')
import os
from django.conf import settings

def delete_media_file(filename):
    full_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
    
def rollBackPics(request):
        try:
            user_id = request.session['id']
            user_data = Candidate.objects.get(userid=user_id)
            first_name = user_data.firstname
            last_name = user_data.lastname
            
            if user_data.profile_pic:
                oldFilename=str(user_data.profile_pic)
                delete_media_file(str(user_data.profile_pic))
                filena,ext=oldFilename.rsplit('-',1)
                try:
                    count,ext=ext.rsplit('.',1)

                except  :  
                    pass
                if int(count)<=1:
                    count=1
                else:
                    count = int(count)-1
            else: 
                count=1
                    
            filename = f"img/{request.session['role']}/{first_name}{last_name}({request.session['email']})/img-{count}.jpg"  # You can adjust the file extension as needed
            
            # Save the picture with the generated filename
            user_data.profile_pic=filename
            user_data.save()
            
            return redirect('profile')
                
        except Candidate.DoesNotExist:
            pass
                
        return redirect('profile')
                    
              
    
def logout_user(request):
    logout(request)
    return redirect('index')


from django.core.paginator import Paginator

def JobList(request):
    joblist = JobDetails.objects.filter(is_active=True).order_by('-id') 

    paginator = Paginator(joblist, 5)  
    page_number = request.GET.get('page')
    
    page_jobs = paginator.get_page(page_number)
    
    
    context = {
        'joblist': page_jobs,
        'job': joblist
        
    }
    
    return render(request, 'joblist.html', context)




def SearchResult(request):
    jobkey = request.GET.get('jobkeyword')
    location = request.GET.get('location')
    
    try:
        joblist = JobDetails.objects.filter(
            Q(is_active=True),
            Q(JobTitle__icontains=jobkey) | Q(JobSkills__icontains=jobkey) | Q(Company_id__CompanyName__icontains=jobkey),
            Q(JobLocation__icontains=location)
        ).order_by('-id')

        paginator = Paginator(joblist, 5)
        page_number = request.GET.get('page')
        page_jobs = paginator.get_page(page_number)

        context = {
            'joblist': page_jobs,
        }

        return render(request, 'searchresult.html', context)
    except:
        joblist = JobDetails.objects.filter(is_active=True).order_by('-id')
        return render(request, 'searchresult.html', {'msg': 'No Jobs found', 'joblist': joblist})


def apply(request,id):
    try:
        if request.session['role']=='Candidate':
            job=JobDetails.objects.get(id=id)
            cand=Candidate.objects.get(userid=request.session['id'])
            context={
                'job':job,
                'user_data':cand
            }
            return render(request, 'apply.html', context)
        else:
            logout(request)
            return render(request, 'login.html', {'msg': 'Please Login first with candidate accout'})

        
                       
    except:
        logout(request)
        return render(request, 'login.html', {'msg': 'Please Login first with candidate accout'})

def SummitApplication(request, id):
    if request.method == 'POST':
        cand = Candidate.objects.get(userid=request.session['id'])
        job = JobDetails.objects.get(id=id)

        
        try:
            existing_application = application.objects.filter(Candidateid=cand, Jobid=job)
            if existing_application:
                
                context = {
                'job': job,
                'user_data': cand,
                'msg': 'You have already applied for this job'
            }
                return render(request, 'apply.html', context)
            
            else:
                resume = request.FILES.get("resume")
                application.objects.create(Candidateid=cand, Resume=resume, Jobid=job)
                context = {
                'job': job,
                'user_data': cand,
                'msg': 'Successfully applied for this job'
                }
                return render(request, 'apply.html', context)
            
            
        except application.DoesNotExist: 
            resume = request.FILES.get("resume")
            application.objects.create(Candidateid=cand, Resume=resume, Jobid=job)
            context = {
                'job': job,
                'user_data': cand,
                'msg': 'Successfully applied for this job'
            }
            return render(request, 'apply.html', context)
        
        
        
def JobDetail(request,id):
    job=JobDetails.objects.get(id=id)
    
    return render(request, 'job-details-2.html',{'job':job})



from django.template.defaulttags import register
@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)
            
def activejob(request,id):
    try:
        job=JobDetails.objects.get(id=id)
        
        job.is_active=True
        job.save()
        
        return redirect('jobpostlist')
    except:
        return redirect('jobpostlist')
              
def deactivatejob(request,id):
        print('deactivate')
        job=JobDetails.objects.get(id=id)
        
        job.is_active=False
        job.save()
        
        return redirect('jobpostlist')
    
    
def Aboutus(request):
    return render(request, 'about.html') 
 
              
               
               
               
               
               
               
               
               
               
               
#  ++++++++++++++++++++ Company views ++++++++++++++++++++++++         
               
                    
                    
                    
                    
def CompanyPage(request):
    try:
        if request.session['method'] == 'POST' and request.session['role'] == 'Company':
            user_data = Company.objects.get(userid_id=request.session['id'])
            job=JobDetails.objects.filter(Company_id=user_data)
            app=application.objects.filter(Jobid__Company_id=user_data)
            active_job_count = JobDetails.objects.filter(is_active=True,Company_id=user_data).count()
            
            context={
                'job': job,
                'user_data': user_data,
                'app':app,
                'active_job_count': active_job_count,
                
            }
            return render(request, 'company/index.html',context)
        else:
            
            return redirect('logout')
        
    except:
        logout(request)
        return render(request,'login.html',{'msg':'Please Login first with company accout'})


def CompanyProfilePage(request):
    try:
        user_id = request.session['id']
        user_data = Company.objects.get(userid=user_id)
        return render(request, 'company/companyprofile.html', {'user_data': user_data})
    
    except Company.DoesNotExist:
        logout(request)
        return render(request, 'login.html', {'msg': 'Please Login'})
    

def UpdateCompanyProfile(request):
    if request.method == 'POST':
        ownername = request.POST.get('ownername')
        if ownername:
            firstname=ownername.split(' ')[0]
            lastname=ownername.split(' ')[1]
            udata.firstname = firstname
            udata.lastname = lastname
        address=request.POST.get('address')
        state=request.POST.get('state')
        companyName=request.POST.get('CompanyName')
        logo_pic=request.FILES.get('logo_pic')
        type=request.POST.get('type')
        founded=request.POST.get('founded')
        services=request.POST.get('services')
        website=request.POST.get('website')
        contact=request.POST.get('contact')
        aboutus=request.POST.get('aboutus')
        
        try:
            udata = Company.objects.get(userid=request.session['id'])
        
                
            
            udata.CompanyName = companyName
            udata.address=address
            udata.type=type
            udata.founded=founded
            udata.services= services
            udata.state=state
            udata.website=website
            udata.contact = contact
            udata.aboutus = aboutus
            if logo_pic:
                udata.logo_pic = logo_pic

            udata.save()
            
            return redirect('companyprofile')
            
        except:
            
            return redirect('signup')
            
def PostJobPage(request):

        if request.session['method'] == 'POST' and request.session['role'] == 'Company':
            user_data = Company.objects.get(userid_id=request.session['id'])
            return render(request, 'company/post_job.html',{'user_data': user_data})
        else:
            logout(request)
            return render(request,'login.html',{'msg':'Please Login first with company accout'})

    # return render(request, 'company/post_job.html')
    
    
def PostJob(request):
    if request.method == 'POST':  # Should be in uppercase 'POST'
        id=request.POST.get('id',0)
        job_title = request.POST.get('jobtitle')
        job_description = request.POST.get('jobdescription')
        job_type = request.POST.get('jobtype')
        job_location = request.POST.get('joblocation')
        min_salary = request.POST.get('minsalary')
        max_salary = request.POST.get('maxsalary')
        job_skills = request.POST.get('jobskills')
        job_experience = request.POST.get('jobexperience')
        job_qualification = request.POST.get('qualification')
        responsibilities = request.POST.get('responsiblities')
        
        # Get the user's Company object based on the session ID
        user = Company.objects.get(userid_id=request.session['id'])
        
        if id:
            try:
                udata = JobDetails.objects.get(id=id)  # Retrieve the job based on the provided ID
                
                udata.JobTitle = job_title
                udata.JobType = job_type
                udata.JobDescription = job_description
                udata.JobLocation = job_location
                udata.minSalary = min_salary
                udata.maxSalary = max_salary
                udata.JobExperience = job_experience
                udata.Qualification = job_qualification
                udata.Responsibilities = responsibilities
                udata.JobSkills = job_skills
                
                udata.save()
            
            
            except JobDetails.DoesNotExist:
            # Handle the case where the provided ID does not exist
                pass
        
        else:
            newjob = JobDetails.objects.create(
                Company_id=user,
                JobTitle=job_title,
                JobType=job_type,
                JobDescription=job_description,
                JobLocation=job_location,
                minSalary=min_salary,
                maxSalary=max_salary,
                Qualification=job_qualification,
                JobExperience=job_experience,
                Responsibilities=responsibilities,
                JobSkills=job_skills
            )
            
        return redirect('jobpostlist')

     
            
        
def JobPostlist(request):

    user_data = Company.objects.get(userid_id=request.session['id'])
    job_details = JobDetails.objects.filter(Company_id=user_data)
    return render(request, 'company/joblist.html', {'job_details': job_details,'user_data':user_data} )

def deletePost(request,id):
    
        
    job_details = JobDetails.objects.get(id=id)
    job_details.delete()
    return redirect('jobpostlist')

def editPost(request,id):
    user_data = Company.objects.get(userid_id=request.session['id'])
    job_detail=JobDetails.objects.get(id=id)
    return render(request, 'company/post_job.html',{"job_detail":job_detail,'user_data':user_data})



def ApplicationList(request):
    user_data = Company.objects.get(userid_id=request.session['id'])
    
    comp = Company.objects.get(userid=request.session['id'])
    jobs = JobDetails.objects.filter(Company_id=comp).order_by('-id')
    
    context = {
        'jobs': jobs,
        "user_data": user_data
        
    }
    return render(request, 'company/applicationlist.html', context)
    