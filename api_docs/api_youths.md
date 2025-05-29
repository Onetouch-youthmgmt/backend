# Youth API Documentation

## Overview
This API provides endpoints for managing Youth records. All endpoints require authentication and appropriate role-based authorization.

## Base URL
`/youths`

## Authentication
- All endpoints require authentication
- All endpoints require either ADMIN or KARYAKARTA role

## Endpoints

### 1. Get All Youths
Retrieves a list of all youths for a specific sabha center.

**Authorization Required:** ADMIN or KARYAKARTA

**Query Parameters:**
- `sabha_center_id` (required): ID of the sabha center to filter youths

### 2. Get Youth by ID

GET /youths/{youth_id}

Retrieves a specific youth by their ID.

**Authorization Required:** ADMIN or KARYAKARTA

### 3. Create New Youth

POST /youths

Creates a new youth record in the system.

**Authorization Required:** ADMIN or KARYAKARTA

### 4. Update Youth

PUT /youths/{youth_id}

Updates an existing youth's information.

**Authorization Required:** ADMIN or KARYAKARTA

**Path Parameters:**
- `youth_id`: ID of the youth to update

### 5. Deactivate Youth

DELETE /youths/{youth_id}

Deactivates a youth record in the system.

**Authorization Required:** ADMIN or KARYAKARTA

**Path Parameters:**
- `youth_id`: ID of the youth to deactivate

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request (e.g., missing sabha_center_id)
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

