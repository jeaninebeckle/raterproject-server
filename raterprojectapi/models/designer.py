from django.db import models


class Designer(models.Model):
    name = models.CharField(max_length=50)