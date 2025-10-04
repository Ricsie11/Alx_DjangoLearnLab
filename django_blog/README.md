# Authentication System Documentation

Overview:

The authentication system is a critical component of the web application, responsible for verifying the identity of users and granting access to protected resources. This documentation provides a detailed overview of the authentication system, including descriptions of each part of the authentication process and instructions on how to test each feature.

Components of the Authentication System
1. User Model
The user model represents an individual user of the application. It stores information such as username, email, and password.

2. Authentication Views
The authentication views handle the logic for user authentication, including login, logout, and password reset.

3. Authentication Forms
The authentication forms provide a way for users to input their credentials and interact with the authentication system.

4. Authentication Templates
The authentication templates render the user interface for the authentication system, including login, logout, and password reset pages.

Authentication Process
1. Registration
Users register for an account by providing a username, email, and password.

2. Login
Users log in to their account by providing their username and password.

3. Authentication
The authentication system verifies the user's credentials and grants access to protected resources if the credentials are valid.

4. Logout
Users log out of their account, ending their session.

Testing the Authentication System
1. Registration Test
1. Go to the registration page.
2. Enter a valid username, email, and password.
3. Click the "Register" button.
4. Verify that the user is redirected to the login page.

2. Login Test
1. Go to the login page.
2. Enter a valid username and password.
3. Click the "Login" button.
4. Verify that the user is redirected to the home page.

3. Logout Test
1. Log in to the application.
2. Click the "Logout" button.
3. Verify that the user is redirected to the login page.

4. Password Reset Test
1. Go to the password reset page.
2. Enter a valid email address.
3. Click the "Reset Password" button.
4. Verify that a password reset email is sent to the user's email address.

Authentication Features
1. Session-Based Authentication
The application uses session-based authentication to store user credentials.

2. Password Hashing
The application uses password hashing to securely store user passwords.

3. Password Reset
The application provides a password reset feature that allows users to reset their password.

Security Considerations
1. Password Storage
The application stores passwords securely using a password hashing algorithm.

2. Session Management
The application uses secure session management practices to prevent session hijacking.

3. CSRF Protection
The application uses CSRF protection to prevent cross-site request forgery attacks.


# Comment System
Functionality
- Add comments to blog posts
- Edit own comments
- Delete own comments
- Superusers/staff can edit/delete any comment

Permissions
- Only logged-in users can comment
- Users can only edit/delete their own comments
- Superusers/staff can edit/delete any comment

API Endpoints
- POST /posts/<int:post_id>/comments/new/: Create comment
- GET/POST /comments/<int:pk>/edit/: Edit comment
- GET/POST /comments/<int:pk>/delete/: Delete comment