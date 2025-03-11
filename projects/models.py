from django.db import models
from config.utlis.base_model import BaseModel


# Create your models here.
class Project(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="projects",
    )

    def __str__(self):
        return self.name
