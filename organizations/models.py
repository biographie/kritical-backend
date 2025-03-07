from django.db import models
from config.utlis.base_model import BaseModel
from users.models import CustomUser


class Organization(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
