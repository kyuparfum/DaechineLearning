from django.db import models

# Create your models here.
class CommonModel(models.Model):
    db_status_choice = [
        (1, 'active'), 
        (2, 'delete'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    db_status = models.PositiveIntegerField(max_length=1, choices=db_status_choice, default=1)
    
    class Meta:
        abstract = True
        # class Meta 를 선언함으로써, 다른 모델들이 상속 받을수 있는 모델이 됨