from django.db import models

# Create your models here.
class Product(models.Model):
     source = models.CharField(max_length=100, default="Modatelas")
     category = models.CharField(max_length=150, blank=True, null=True)
     name = models.CharField(max_length=300, blank=True, null=True)
     price = models.CharField(max_length=50, blank=True, null=True)
     url = models.URLField(max_length=500, blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     
     class Meta: 
          ordering = ['-created_at']
          
     def __str__(self):
          return f"{self.name} - {self.source}"