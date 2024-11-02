from django.db import models

class Code(models.Model):
    code = models.TextField(max_length=5000)
    input_d = models.TextField(max_length=5000, default="")