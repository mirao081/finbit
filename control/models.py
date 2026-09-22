from django.db import models


class AdminDashboardSettings(models.Model):

    title = models.CharField(
        max_length=100,
        default="Finbit Admin Dashboard"
    )

    logo = models.ImageField(
        upload_to="admindash/images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class AdminMenu(models.Model):

    name = models.CharField(
        max_length=50
    )

    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class, e.g. 'fas fa-chart-line'"
    )

    url_name = models.CharField(
        max_length=100
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name