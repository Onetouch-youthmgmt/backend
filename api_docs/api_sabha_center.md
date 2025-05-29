# Sabha Centers API Documentation

## Overview
This API provides endpoints for managing Sabha Centers. All endpoints require authentication and appropriate role-based authorization.

## Base URL
`/sabha_centers`

## Authentication
- All endpoints require authentication
- Most endpoints require either ADMIN or KARYAKARTA role
- Delete endpoint requires ADMIN role only

## Endpoints

### 1. Get All Sabha Centers

GET /sabha_centers

Retrieves a list of all sabha centers in the system.

**Authorization Required:** ADMIN or KARYAKARTA

### 2. Get Sabha Center by ID

GET /sabha_centers/{sabha_center_id}

Retrieves a specific sabha center by its ID.

**Authorization Required:** ADMIN or KARYAKARTA

**Path Parameters:**
- `sabha_center_id`: ID of the sabha center to retrieve

### 3. Create New Sabha Center

POST /sabha_centers

Creates a new sabha center in the system.

**Authorization Required:** ADMIN or KARYAKARTA

### 4. Update Sabha Center

PUT /sabha_centers/{sabha_center_id}

Updates an existing sabha center's information.

**Authorization Required:** ADMIN or KARYAKARTA

**Path Parameters:**
- `sabha_center_id`: ID of the sabha center to update

### 5. Delete Sabha Center

DELETE /sabha_centers/{sabha_center_id}

Deletes a sabha center from the system.

**Authorization Required:** ADMIN only

**Path Parameters:**
- `sabha_center_id`: ID of the sabha center to delete

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
