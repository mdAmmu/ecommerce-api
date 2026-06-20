# Post 1: Project Setup & Authentication

## LinkedIn Post

**I'm building an E-Commerce API from scratch using FastAPI + Python**

Today I set up the foundation of my project. Here's what I built:

1. Bootstrapped a FastAPI app with proper folder structure
2. Connected it to a PostgreSQL database using SQLAlchemy
3. Built a full user authentication system:
   - Register (sign up with email & password)
   - Login (get JWT access + refresh tokens)
   - Refresh token (get a new access token without logging in again)
   - Logout (blocklist the token so it can't be reused)

The key thing I learned? Always hash passwords before storing them. Never store plain text passwords in your database.

Tech stack: Python, FastAPI, PostgreSQL, SQLAlchemy, JWT

Building in public. More updates coming soon!

#FastAPI #Python #BackendDevelopment #LearnInPublic #API #PostgreSQL

---

## Image Prompt

"A clean, modern flat illustration of a login/authentication flow diagram. Show a user icon on the left, arrows going to a server icon in the middle, and a database icon on the right. Include small labels: 'Register', 'Login', 'JWT Token', 'Database'. Use a dark blue and green color scheme with a white background. Minimalist tech style, no text heavy."
