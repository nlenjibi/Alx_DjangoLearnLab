# API Authentication and Testing Guide

## Overview

This Django REST Framework API now includes token-based authentication and permission controls. All endpoints require authentication except for the token retrieval endpoint.

## Authentication Setup

### 1. Database Migration

Before testing, run migrations to create authentication tables:

```bash
python manage.py migrate
```

### 2. Create Test Users

Run the management command to create test users:

```bash
python manage.py create_test_users
```

This will create:

- **testuser** (regular user) - Password: `testpass123`
- **admin** (admin user) - Password: `adminpass123`

## API Endpoints

### Authentication Endpoint

#### Get Authentication Token

- **URL**: `POST /api/auth/token/`
- **Description**: Obtain authentication token
- **Body**:

```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

- **Response**:

```json
{
  "token": "your_token_here",
  "user_id": 1,
  "username": "testuser",
  "email": "testuser@example.com"
}
```

### Book Endpoints (All require authentication)

#### List All Books

- **URL**: `GET /api/books_all/`
- **Headers**: `Authorization: Token your_token_here`
- **Description**: Get all books (paginated)

#### Create a Book

- **URL**: `POST /api/books_all/`
- **Headers**: `Authorization: Token your_token_here`
- **Body**:

```json
{
  "title": "New Book Title",
  "author": "Author Name",
  "published_date": "2025-01-01",
  "isbn": "1234567890123"
}
```

#### Get Specific Book

- **URL**: `GET /api/books_all/{id}/`
- **Headers**: `Authorization: Token your_token_here`

#### Update a Book

- **URL**: `PUT /api/books_all/{id}/`
- **Headers**: `Authorization: Token your_token_here`
- **Body**: (same as create)

#### Partially Update a Book

- **URL**: `PATCH /api/books_all/{id}/`
- **Headers**: `Authorization: Token your_token_here`
- **Body**: (any subset of book fields)

#### Delete a Book

- **URL**: `DELETE /api/books_all/{id}/`
- **Headers**: `Authorization: Token your_token_here`

#### List Books (Alternative endpoint)

- **URL**: `GET /api/books/`
- **Headers**: `Authorization: Token your_token_here`

## Testing with cURL

### 1. Get Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 2. List Books (with token)

```bash
curl -X GET http://localhost:8000/api/books_all/ \
  -H "Authorization: Token your_token_here"
```

### 3. Create Book (with token)

```bash
curl -X POST http://localhost:8000/api/books_all/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "published_date": "2025-01-01",
    "isbn": "1234567890123"
  }'
```

### 4. Test without token (should fail)

```bash
curl -X GET http://localhost:8000/api/books_all/
```

## Testing with Postman

### 1. Get Token

- Method: `POST`
- URL: `http://localhost:8000/api/auth/token/`
- Body (JSON):

```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

### 2. Use Token for API Calls

- Add Header: `Authorization: Token your_token_here`
- Make requests to any book endpoint

## Permission Classes Used

1. **IsAuthenticated**: Requires user to be logged in
2. **Custom permissions** in ViewSet based on action type

## Error Responses

### 401 Unauthorized (No token)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Unauthorized (Invalid token)

```json
{
  "detail": "Invalid token."
}
```

### 403 Forbidden (No permission)

```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Notes

- Tokens don't expire by default in DRF
- Each user has one token
- If you lose a token, you can get a new one by calling the token endpoint again
- All book operations now require authentication
- The API uses pagination for list views (20 items per page)
