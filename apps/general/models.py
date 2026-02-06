from django.db import models
from uuid import uuid4

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Обновлено время", null=True, blank=True)
    uuid = models.UUIDField(verbose_name="Уникальный ID (UUID)",
                            unique=True, editable=False)
    is_active = models.BooleanField(verbose_name="Активен", null=True, 
                                    blank=True, default=True)
    
    def save(self, *args, **kwargs):
        unique_uuid = uuid4()
        
        while self.__class__.objects.filter(uuid=unique_uuid).exists() is True:
            unique_uuid = uuid4()
        self.uuid = unique_uuid

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True