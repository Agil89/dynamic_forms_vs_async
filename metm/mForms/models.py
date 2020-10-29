from django.db import models


class Forms(models.Model):
    name = models.CharField('Name',max_length=1024)

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField('is published', default=False)

    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'

    def __str__(self):
        return f'{self.name}'

class Fields(models.Model):
    choices_for_field=[
        ('1','TextArea'),
        ('2', 'Integer'),
        ('3', 'DateTime'),
        ('4', 'Date'),
        ('5','Text'),
        ('6','Selector'),
        ('7','Email')]
    choices_for_validation=[
        ('1','Text'),
        ('2','Email'),
        ('3','Integer')
    ]
    #relations
    forms = models.ForeignKey(Forms,verbose_name='Forms',on_delete=models.CASCADE,null=True,blank=True,db_index=True,related_name='fields')

    #information
    label = models.CharField('Label',max_length=256)
    type = models.CharField('Type',max_length=2,choices=choices_for_field)
    default_value=models.CharField('Default Value',max_length=1024,null=True,blank=True)
    required = models.BooleanField('Is required',default=False)
    validation = models.CharField('VAlidation',max_length=2,choices=choices_for_validation)

    #moderation
    is_published = models.BooleanField('is published',default=False)

    def __str__(self):
        return f'{self.label}'

class Values(models.Model):
    #realtions
    forms = models.ForeignKey(Forms, verbose_name='Forms', on_delete=models.CASCADE, null=True, blank=True,
                              db_index=True, related_name='values')
    form_fields = models.ForeignKey(Fields,verbose_name='Fields',on_delete=models.CASCADE,null=True,blank=True,db_index=True,related_name='values')

    #information
    value = models.TextField('Value',max_length=1024)

class SendList(models.Model):
    # realtions
    forms = models.ForeignKey(Forms,verbose_name='Forms',on_delete=models.CASCADE,null=True,blank=True,db_index=True,related_name='sendlist')

    #information
    email = models.CharField('Email',max_length=120)

    class Meta:
        verbose_name = 'SendList'
        verbose_name_plural = 'SendLists'

    def __str__(self):
        return f'{self.email}'