# Post 3: Get User Profile (Protected Route)

## LinkedIn Post

**Not every API endpoint should be open to everyone.**

Today I built my first protected route in FastAPI: **GET /users/me**

This endpoint returns the logged-in user's profile. But here's the catch - you can only access it if you send a valid JWT token.

No token? You get a 401 Unauthorized error.
Expired token? Same thing.
Valid token? Welcome, here's your profile!

How I did it:
- Created a `get_current_user` dependency in FastAPI
- It reads the token from the request header
- Decodes it and finds the user in the database
- If everything checks out, the endpoint works

This is how real apps protect user data. One small function, big security impact.

#FastAPI #Python #APIDevelopment #WebSecurity #BuildInPublic #BackendEngineering

---

## Image Prompt

"A flat design illustration showing a shield/lock protecting an API endpoint. On the left, two paths: one with a green checkmark showing a user with a valid token getting access to their profile data, and one with a red X showing an unauthorized user being blocked. Clean minimal style, dark blue and green colors, white background, professional tech look."
