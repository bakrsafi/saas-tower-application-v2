from django.db import models


# =====================================================
# Projects
# =====================================================

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="projects/logos/",
        blank=True,
        null=True
    )

    brochure = models.FileField(
        upload_to="projects/brochures/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name


# =====================================================
# Buildings
# =====================================================

class Building(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="buildings"
    )

    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    total_floors = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "buildings"

    def __str__(self):
        return self.name


# =====================================================
# Apartments
# =====================================================

class Apartment(models.Model):

    STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("sold", "Sold"),
    ]

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="apartments"
    )

    unit_number = models.CharField(max_length=50)

    floor_number = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    area_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    bedrooms = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    bathrooms = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "apartments"

    def __str__(self):
        return self.unit_number


# =====================================================
# Building Images
# =====================================================

class BuildingImage(models.Model):

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="buildings/images/"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    rotation = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    # 0
    # 45
    # 90
    # 135
    # 180
    # ...

    sort_order = models.PositiveIntegerField(
        default=0
    )

    width = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    height = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

# =====================================================
# Apartment Media
# =====================================================

class ApartmentMedia(models.Model):

    MEDIA_TYPES = [
        ("image", "Image"),
        ("video", "Video"),
        ("pdf", "PDF"),
        ("panorama", "Panorama"),
    ]

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="media"
    )

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES
    )

    file = models.FileField(
        upload_to="apartments/media/"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "apartment_media"

    def __str__(self):
        return self.title or self.file.name


# =====================================================
# Apartment Polygons
# =====================================================

class ApartmentPolygon(models.Model):

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="polygons"
    )

    building_image = models.ForeignKey(
        BuildingImage,
        on_delete=models.CASCADE,
        related_name="polygons"
    )

    polygon = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "apartment_polygons"

    def __str__(self):
        return f"{self.apartment.unit_number}"