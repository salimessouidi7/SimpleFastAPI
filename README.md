Simple FastAPI
This is a simple FastAPI project that provides API endpoints for user authentication and CRUD operations on user data.

Installation
1-Clone the repository:
git clone https://github.com/salimessouidi7/SimpleFastAPI.git

2-Install the dependencies:
pip install -r requirements.txt

Usage
1-Run the FastAPI application:
uvicorn main:app --reload

Visit http://localhost:8000/docs in your browser to view the interactive API documentation.

API Endpoints
POST /login: Endpoint for user login.
POST /register: Endpoint for user registration.
GET /user: Endpoint to get user by ID.
PUT /user: Endpoint to update user information.
PATCH /user: Endpoint to partially update user information.
DELETE /user: Endpoint to delete user.

Contributing
Contributions are welcome! Here's how you can contribute:

Fork the repository
Create a new branch (git checkout -b feature)
Make your changes
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature)
Create a pull request
