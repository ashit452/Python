from django.db import models
from django.db import transaction

# Create your models here.
class option(models.Model):
    optionId = models.AutoField(primary_key=True)
    customOption = models.CharField(("Custom Option"),max_length=100,unique=True)
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    isDefault = models.BooleanField(("Is Default"),default=False)

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(option, self).save(*args, **kwargs)
        with transaction.atomic():
            option.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(option, self).save(*args, **kwargs)