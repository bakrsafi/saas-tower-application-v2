from rest_framework import viewsets

from .models import (
    Project,
    Building,
    Apartment,
)

from .serializers import (
    ProjectSerializer,
    BuildingSerializer,
    ApartmentSerializer,
)



# ==============================
# Project API
# ==============================

class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()

    serializer_class = ProjectSerializer



# ==============================
# Building API
# ==============================

class BuildingViewSet(viewsets.ModelViewSet):

    queryset = Building.objects.all()

    serializer_class = BuildingSerializer



# ==============================
# Apartment API
# ==============================

class ApartmentViewSet(viewsets.ModelViewSet):

    queryset = Apartment.objects.all()

    serializer_class = ApartmentSerializer