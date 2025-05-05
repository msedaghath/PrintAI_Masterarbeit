# Accounts Module

## Overview

The Accounts module handles all user authentication, registration, and profile management functionality for the PrintAI Dashboard. This module is part of the architectural refactoring to improve code organization and maintainability.

## Features

- User registration and authentication
- Profile management
- Session handling

## Models

- `Profile`: Extends the Django User model with additional fields for organization information and user preferences

## Views

- `SignUpView`: User registration view
- `LoginView`: User authentication view
- `UserAccountView`: Profile management view
- `logout_user`: User logout functionality

## URLs

- `/accounts/signup/`: User registration
- `/accounts/login/`: User authentication
- `/accounts/logout/`: User logout
- `/accounts/profile/`: Profile management

## Templates

- `signup.html`: User registration form
- `login.html`: Login form
- `user_account.html`: Profile management form

## Usage

This module is designed to be used as part of the PrintAI Dashboard system. It handles all user-related functionality and integrates with the other modules.

## Dependencies

- Django's built-in authentication system
- Custom validators from the core module