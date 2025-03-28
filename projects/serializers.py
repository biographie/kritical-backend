from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'organization']  # Explicitly specify fields
        read_only_fields = ['organization']  # Organization is set in perform_create

    def validate(self, data):
        print("Validating data:", data)  # Debug print
        return data
