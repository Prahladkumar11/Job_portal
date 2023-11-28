from django.db import models

# Create your models here.
class UserMaster(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    otp=models.IntegerField()
    role=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    is_updated=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
class ContactData(models.Model):
    Name=models.CharField( max_length=50)
    Email=models.EmailField( max_length=254)
    Sub=models.CharField(max_length=250)
    Msg=models.CharField(max_length=500)
    
class Candidate(models.Model):
    userid=models.ForeignKey(UserMaster, on_delete=models.CASCADE,related_name='candidates')
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    dob=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="img/Candidate")
    education=models.CharField(max_length=50,null=True ,blank=True)
    website=models.CharField( max_length=200,null=True,blank=True)
    
    
    def __str__(self):
        return self.firstname + " " + self.lastname
    
class Company(models.Model):
    userid=models.ForeignKey(UserMaster, on_delete=models.CASCADE,related_name='companies')
    CompanyName=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    logo_pic=models.ImageField(upload_to="img/Company",default='img/default/d2.png')
    website=models.CharField( max_length=200,null=True,blank=True)
    type=models.CharField(max_length=50,null=True,blank=True)
    services=models.CharField(max_length=1000,null=True,blank=True)
    aboutus=models.TextField(null=True,blank=True)
    founded=models.IntegerField(null=True,blank=True)
    
  
    def __str__(self):
        return self.CompanyName
    

   
class JobDetails(models.Model):
    Company_id=models.ForeignKey(Company, on_delete=models.CASCADE)
    JobTitle=models.CharField(max_length=250)
    JobType=models.CharField(max_length=250)
    JobDescription=models.TextField()
    JobLocation=models.CharField(max_length=250)
    minSalary=models.CharField(max_length=10)
    maxSalary=models.CharField(max_length=10)
    JobExperience=models.IntegerField()
    Qualification=models.TextField(null=True)
    Responsibilities=models.TextField(null=True)
    JobSkills=models.CharField(max_length=300)
    PostDate = models.DateField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.JobTitle} , {self.Company_id.CompanyName}, {self.is_active}"
    
class application(models.Model):
    Jobid=models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    Candidateid=models.ForeignKey(Candidate, on_delete=models.CASCADE)
    Resume=models.FileField(upload_to="Resume/")
    
    def __str__(self) -> str:
        return f"{self.Candidateid.firstname},{self.Jobid.JobTitle}-{self.Jobid.Company_id.CompanyName}"
    

