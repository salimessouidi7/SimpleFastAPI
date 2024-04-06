# Simple FastAPI

This is a simple FastAPI project that provides API endpoints for user authentication and CRUD operations on user data.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/salimessouidi7/SimpleFastAPI.git
```
2. Install the dependencies:

```bash
pip install -r requirements.txt
```
## Usage

1. Run the FastAPI application:

```bash
uvicorn authenticationMongoDB:app --reload
```
2. Visit http://localhost:8000/docs in your browser to view the interactive API documentation.

## API Endpoints

### POST /login
Endpoint for user login.

### POST /register
Endpoint for user registration.

### GET /user
Endpoint to get user by ID.

### PUT /user
Endpoint to update user information.

### PATCH /user
Endpoint to partially update user information.

### DELETE /user
Endpoint to delete user.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a new branch** (`git checkout -b feature`)
3. **Make your changes**
4. **Commit your changes** (`git commit -am 'Add new feature'`)
5. **Push to the branch** (`git push origin feature`)
6. **Create a pull request**

## Technology Stack

- **FastAPI**: FastAPI is used as the web framework for building the API endpoints.

