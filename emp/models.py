from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
import uuid
#from django.utils.safestring import mark_safe

# Model of employee, which has chief(same as employee) recourse to itself.

class Employee(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=128, verbose_name='surname, name, fathers', unique=True, db_index=True)
    emp_position = models.CharField(max_length=50)
    chief = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, max_length=128,
                           verbose_name='chief', blank=True, related_name='children', db_index=True)
    date_of_recruit = models.DateTimeField()
    salary = models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='salary', db_index=True)
    photo = models.ImageField(upload_to='', verbose_name=u'Photo', help_text='jpg/png - file', blank=True)

    class MPTTMeta:
        parent_attr = 'chief'
        level_attr = 'level'
        order_insertion_by = ['full_name', 'date_of_recruit']

    def __str__(self):
        return self.full_name

    def photo_src(self):
        if self.photo:
            return '<img src="{0}" width="30"/>'.format(self.photo.url)

    photo_src.allow_tags = True
