# Validation Document

## Overview

This document defines the validation rules for all **Create APIs** related to:

- Projects
- Buildings
- Apartments
- Building Images
- Apartment Media
- Apartment Polygons

---

# 1. Project

## Endpoint

`POST /api/projects/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| name | string | ✅ | Required, 3–255 characters |
| description | string | ❌ | Maximum 5000 characters |
| country | string | ❌ | Maximum 100 characters |
| city | string | ❌ | Maximum 100 characters |
| address | string | ❌ | Maximum 1000 characters |
| logo | image | ❌ | jpg, jpeg, png, webp, max 5 MB |
| brochure | file | ❌ | PDF only, max 20 MB |

### Business Rules

- Project name should be unique.
- Trim leading/trailing whitespace from all text fields.

---

# 2. Building

## Endpoint

`POST /api/buildings/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| project | integer | ✅ | Existing Project ID |
| name | string | ✅ | Required, max 255 characters |
| description | string | ❌ | Maximum 5000 characters |
| total_floors | integer | ❌ | Positive integer, minimum 1 |

### Business Rules

- Project must exist.
- Building name should be unique within the same project.

### Example

Allowed

```
Project A
 ├── Building A
 └── Building B

Project B
 └── Building A
```

Not Allowed

```
Project A
 ├── Building A
 └── Building A
```

---

# 3. Apartment

## Endpoint

`POST /api/apartments/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| building | integer | ✅ | Existing Building ID |
| unit_number | string | ✅ | Required, max 50 characters |
| floor_number | integer | ❌ | Positive integer |
| area_m2 | decimal | ❌ | Greater than 0 |
| bedrooms | integer | ❌ | Minimum 0 |
| bathrooms | integer | ❌ | Minimum 0 |
| price | decimal | ❌ | Greater than or equal to 0 |
| status | enum | ❌ | available, reserved, sold |
| description | string | ❌ | Maximum 5000 characters |

### Business Rules

- Building must exist.
- Unit number should be unique within the same building.

### Example

Allowed

```
Building A
101
102
103

Building B
101
```

Not Allowed

```
Building A
101
101
```

---

# 4. Building Image

## Endpoint

`POST /api/building-images/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| building | integer | ✅ | Existing Building ID |
| image | image | ✅ | jpg, jpeg, png, webp, max 10 MB |
| title | string | ❌ | Maximum 255 characters |
| rotation | decimal | ❌ | Value between 0 and 360 |
| sort_order | integer | ❌ | Minimum 0 |
| width | integer | ❌ | Positive integer |
| height | integer | ❌ | Positive integer |

### Business Rules

- Building must exist.
- Image is required.

---

# 5. Apartment Media

## Endpoint

`POST /api/apartment-media/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| apartment | integer | ✅ | Existing Apartment ID |
| media_type | enum | ✅ | image, video, pdf, panorama |
| file | file | ✅ | File must match media type |
| title | string | ❌ | Maximum 255 characters |
| sort_order | integer | ❌ | Minimum 0 |

## File Validation

### Image

Supported formats

```
jpg
jpeg
png
webp
```

Maximum size

```
10 MB
```

---

### Video

Supported formats

```
mp4
mov
avi
mkv
```

Maximum size

```
500 MB
```

---

### PDF

Supported formats

```
pdf
```

Maximum size

```
20 MB
```

---

### Panorama

Supported formats

```
jpg
jpeg
png
```

Recommended aspect ratio

```
2:1
```

Maximum size

```
20 MB
```

### Business Rules

- Apartment must exist.
- Uploaded file must match the selected media type.

Examples

Invalid

```json
{
  "media_type": "image",
  "file": "document.pdf"
}
```

Invalid

```json
{
  "media_type": "pdf",
  "file": "image.jpg"
}
```

---

# 6. Apartment Polygon

## Endpoint

`POST /api/apartment-polygons/`

### Fields

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| apartment | integer | ✅ | Existing Apartment ID |
| building_image | integer | ✅ | Existing Building Image ID |
| polygon | JSON | ✅ | Valid polygon coordinates |

## Polygon Validation

The polygon must be an array of points.

Example

```json
[
  { "x": 10, "y": 20 },
  { "x": 200, "y": 20 },
  { "x": 180, "y": 90 },
  { "x": 20, "y": 80 }
]
```

Rules

- Minimum of **3 points**.
- Every point must contain numeric `x` and `y`.
- Coordinates must be within the image boundaries (if width and height are available).
- The selected `building_image` must belong to the same building as the apartment.

---

# General Validation Rules

## Text Fields

- Trim leading and trailing whitespace.
- Reject empty values for required fields.

---

## Numeric Fields

- Must contain valid numeric values.
- Positive fields cannot be negative.
- Decimal fields must respect model precision.

---

## Foreign Keys

- Referenced object must exist.
- Invalid IDs should return:

```http
400 Bad Request
```

or

```http
404 Not Found
```

depending on the API design.

---

## Validation Error Format

```json
{
  "errors": {
    "name": [
      "This field is required."
    ],
    "price": [
      "Price must be greater than or equal to zero."
    ]
  }
}
```

---

# Recommended Database Constraints

## Project

- `Project.name` should be unique.

## Building

Unique within the same project.

```python
UniqueConstraint(
    fields=["project", "name"],
    name="unique_building_per_project"
)
```

## Apartment

Unique within the same building.

```python
UniqueConstraint(
    fields=["building", "unit_number"],
    name="unique_unit_per_building"
)
```

## Apartment Polygon

Validate that the selected `building_image` belongs to the same building as the apartment before saving.