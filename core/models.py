from django.db import models
from django.core.exceptions import ValidationError


class ApplicationAuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    object_changed = models.CharField(max_length=60)
    object_type = models.CharField(max_length=50)
    changed_by = models.CharField(max_length=50)
    old_value = models.JSONField()
    new_value = models.JSONField()
    message = models.TextField()

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f'{self.timestamp} | {self.object_type} | {self.object_changed}'

    def save(self, *args, **kwargs):
        # If the instance has an id, then it's not a new object
        if self.pk:
            raise ValidationError("Records in Document model cannot be modified once created.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Records in Document model cannot be deleted.")