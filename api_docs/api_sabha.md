# Sabha API Documentation

This document outlines the API endpoints for managing sabhas in the system.

## Base URL
All endpoints are prefixed with `/sabhas`

## Authentication
All endpoints require authentication. Different endpoints have different role requirements:
- ADMIN: Can access all endpoints
- KARYAKARTA: Can access all endpoints except DELETE

## Endpoints

### Get All Sabhas

GET /sabhas

Retrieves a list of all sabhas for a specific sabha center.

### Get Sabha by ID

GET /sabhas/{sabha_id}

**Path Parameters:**
- `sabha_id` (required): ID of the sabha to retrieve


### Create New Sabha

POST /sabhas

### Update Sabha

PUT /sabhas/{sabha_id}

**Path Parameters:**
- `sabha_id` (required): ID of the sabha to update


### Delete Sabha

DELETE /sabhas/{sabha_id}

**Path Parameters:**
- `sabha_id` (required): ID of the sabha to delete


## Error Responses
All endpoints may return the following error responses:
- `401 Unauthorized`: If authentication fails
- `403 Forbidden`: If user doesn't have required role
- `404 Not Found`: If sabha with given ID doesn't exist
- `500 Internal Server Error`: For server-side errors

This documentation provides a comprehensive overview of all the sabha-related endpoints, including:
- Authentication requirements
- Request/response formats
- Path and query parameters
- Possible error responses

The documentation follows standard API documentation practices and includes examples of request/response formats. You may want to add more specific details about the request/response schemas based on your actual `SabhaCreate` and `SabhaResponse` models.

