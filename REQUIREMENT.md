# Ecommerce Backend Requirements

## Purpose

The Ecommerce Backend provides functionality for customer accounts, product browsing, shopping carts, order processing, payments, inventory management, and administrative operations.

This document defines business behaviour and serves as the source of truth for application requirements.

---

# 1. User Management

## Registration

Users can create an account using:

- First Name
- Last Name
- Email Address
- Password

### Rules

- Email must be unique.
- Email must be valid.
- Password must be at least 8 characters.
- Password must contain at least:
  - One uppercase letter
  - One lowercase letter
  - One number
- Registration fails if email already exists.

## Login

Users can log in using:

- Email
- Password

### Rules

- Login fails for invalid credentials.
- Login succeeds only for active accounts.
- Successful login creates an authenticated session/token.

## Logout

Users can log out from the application.

### Rules

- Existing authentication token/session becomes invalid.
- User must log in again to access protected resources.

## Password Reset

Users can request a password reset.

### Flow

1. User enters email.
2. System sends reset link/token.
3. User submits new password.
4. Password is updated.

### Rules

- Reset token expires after a defined period.
- Token can only be used once.

## Profile Management

Users can:

- View profile
- Update profile details

Allowed updates:

- First Name
- Last Name
- Phone Number
- Address

Email changes require verification.

---

# 2. Product Management

## Product Fields

Every product contains:

- Name
- Description
- SKU
- Price
- Stock Quantity
- Category
- Images
- Status (Active/Inactive)
- Created Date
- Updated Date

## Product Creation

Admins can create products.

### Rules

- Product name is required.
- SKU must be unique.
- Price must be greater than zero.
- Initial stock quantity must be zero or greater.

## Product Updates

Admins can update any product field.

## Product Deletion

Products are soft deleted.

### Rules

- Deleted products are hidden from customers.
- Historical order records remain unchanged.

## Product Listing

Users can:

- Browse products
- Filter products
- Sort products

Available filters:

- Category
- Price Range
- Availability

## Product Search

Users can search by:

- Product Name
- SKU

Search is case-insensitive.

---

# 3. Category Management

## Category Fields

- Name
- Description
- Status

## Category Creation

Admins can create categories.

Category names must be unique.

## Category Updates

Admins can update category details.

## Category Deletion

Categories cannot be deleted if products are assigned.

### Rules

Admin must:

- Move products to another category
- Or remove products first

This prevents orphaned products.

---

# 4. Cart Management

## Add To Cart

Users can add products to cart.

### Rules

- Product must be active.
- Product must have available stock.
- Quantity must be greater than zero.

## Quantity Updates

Users can increase or decrease quantity.

### Rules

- Quantity cannot exceed available stock.
- Quantity cannot be less than one.

## Remove Item

Users can remove individual items.

## Clear Cart

Users can remove all items.

## Cart Totals

Cart total consists of:

- Product subtotal
- Tax
- Shipping cost (if applicable)

Formula:

Total = Subtotal + Tax + Shipping

---

# 5. Order Management

## Order Creation

An order is created when payment is successfully verified.

## Order States

Orders move through:

Pending
→ Processing
→ Shipped
→ Delivered

Alternative state:

Pending
→ Cancelled

## Cancellation Rules

Users may cancel only when order status is:

- Pending

Admins may cancel:

- Pending
- Processing

Shipped and Delivered orders cannot be cancelled.

## Order History

Users can:

- View order history
- View order details

---

# 6. Payment Management

## Payment Initiation

Payment begins during checkout.

### Flow

1. User reviews order
2. User submits payment
3. Payment provider processes request

## Payment Verification

Order is confirmed only after successful payment verification.

### Rules

- Failed payments do not create completed orders.
- Duplicate payment confirmations are ignored.

## Refund Rules

Refunds may be issued when:

- Order is cancelled before shipment
- Admin approves refund

Refund requests are recorded for auditing.

---

# 7. Inventory Management

## Stock Tracking

Each product maintains available stock quantity.

## Stock Deduction

Stock is deducted when:

- Payment is verified
- Order is successfully created

## Stock Restoration

Stock is restored when:

- Order is cancelled
- Refund is approved

## Low Stock

Products with zero stock:

- Remain visible
- Display Out of Stock

## Edge Case: Stock Runs Out During Checkout

If stock becomes unavailable before payment verification:

- Order creation fails
- User receives an out-of-stock message
- Payment is not captured

---

# 8. Admin Management

## Admin Access

Admins have access to:

- User Management
- Product Management
- Category Management
- Inventory Management
- Order Management
- Payment Monitoring

## User Management

Admins can:

- View users
- Disable users
- Reactivate users

Admins cannot view user passwords.

## Product Management

Admins can:

- Create products
- Update products
- Deactivate products

## Inventory Management

Admins can:

- View stock
- Adjust stock
- Track stock changes

## Order Management

Admins can:

- View all orders
- Update order status
- Cancel eligible orders

## Reporting

Admins can view:

- Sales reports
- Inventory reports
- Order statistics

---

# General Business Rules

## Authentication Required

The following actions require authentication:

- Cart operations
- Order creation
- Order history
- Profile updates

## Authorization

Regular users can access only their own data.

Admins can access administrative functionality.

## Auditability

Important actions should be logged:

- Product creation
- Product updates
- Inventory changes
- Order status changes
- Refund actions