# Post 2: JWT Tokens & Security

## LinkedIn Post

**How does your app know you're logged in? JWT Tokens.**

While building my E-Commerce API, I learned how JWT (JSON Web Tokens) actually work. Let me explain it simply:

When you login, the server gives you 2 tokens:
- **Access Token** - Short-lived (30 min). You send this with every request to prove who you are.
- **Refresh Token** - Long-lived (7 days). Use it to get a new access token without logging in again.

When you logout, the token gets added to a "blocklist" so nobody can reuse it.

Think of it like a movie ticket:
- Access token = your ticket to enter the hall
- Refresh token = your receipt to get a replacement ticket
- Logout = tearing up the ticket so it can't be used again

Simple concept, powerful security.

#JWT #APISecurity #FastAPI #Python #BackendDeveloper #LearningToCode

---

## Image Prompt

"A simple infographic showing how JWT tokens work. Left side shows a user logging in, middle shows two tokens labeled 'Access Token (30 min)' and 'Refresh Token (7 days)' with lock icons, right side shows a blocked/crossed-out token for logout. Use a clean blue and orange color palette, flat design style, white background, professional and easy to understand."
