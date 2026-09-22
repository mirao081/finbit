fromdjango.dbimportmodels

classAdminDashboardSettings(models.Model):
    title=models.CharField(max_length=100,default="Finbit Admin Dashboard")
logo=models.ImageField(upload_to='admindash/images/',blank=True,null=True)

def__str__(self):
        returnself.title


classAdminMenu(models.Model):
    name=models.CharField(max_length=50)
icon=models.CharField(max_length=50,help_text="FontAwesome icon class, e.g. 'fas fa-chart-line'")
url_name=models.CharField(max_length=100)
order=models.PositiveIntegerField(default=0)

classMeta:
        ordering=["order"]

def__str__(self):
        returnself.name

