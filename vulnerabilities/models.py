from django.db import models

class Vulnerability(models.Model):
    
    class Meta:
        db_table = 'vulnerabilities'
        
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    cve_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    severity = models.CharField(max_length=50)
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id
