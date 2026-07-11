from rest_framework import serializers

from .models import (
    Project,
    Building,
    Apartment,
)


# ==============================
# Apartment Serializer
# ==============================

class ApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartment
        fields = "__all__"



# ==============================
# Building Serializer
# ==============================

class BuildingSerializer(serializers.ModelSerializer):

    apartments = ApartmentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Building
        fields = [
            "id",
            "project",
            "name",
            "description",
            "total_floors",
            "apartments",
            "created_at",
            "updated_at",
        ]



# ==============================
# Project Serializer
# ==============================

class ProjectSerializer(serializers.ModelSerializer):

    buildings = BuildingSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "country",
            "city",
            "address",
            "logo",
            "brochure",
            "buildings",
            "created_at",
            "updated_at",
        ]