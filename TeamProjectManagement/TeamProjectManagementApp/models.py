from django.db import models

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
            return self.team_name
    
class Membership(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "-"+ self.team.team_name

class Tasks(models.Model):
     task_name = models.CharField(max_length = 150)
     description = models.CharField(max_length = 500)
     team = models.ForeignKey(Team,on_delete=models.CASCADE)
     assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     deadline = models.DateTimeField()
     completed_at = models.DateTimeField(null=True,blank=True)
     choices = [
        ("pending", "Pending"),('inprogress',"InProgress"),('completed','Completed')]
     status = models.CharField(max_length=20, choices=choices,default='pending')
     choices = [("low","Low",),("medium","Medium"),("high","High")]
     priority = models.CharField(max_length = 20,choices = choices,default = 'medium')

     def __str__(self):
         return self.task_name
