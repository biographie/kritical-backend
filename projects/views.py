from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(organization=user.organization)


class ProjectCreateView(generics.CreateAPIView):    
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        print("Request user:", self.request.user)
        print("Request data:", self.request.data)  # See the incoming data
        try:
            user = self.request.user
            serializer.save(organization=user.organization)
        except Exception as e:
            print("Error saving project:", str(e))  # See any validation errors
            raise

