from django.db import models

class Code(models.Model):
    code = models.TextField(max_length=5000)