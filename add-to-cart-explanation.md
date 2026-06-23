# Add to Cart - Complete Code Explanation

## The Big Picture

When a user sends `POST /cart/items` with `{"product_id": 5, "quantity": 2}`, the request flows through these layers:

```
User Request
    ↓
Route (app/api/cart.py)          → "Who is this user? Pass data to service"
    ↓
Schema (app/schemas/cart.py)     → "Is the data valid? quantity > 0?"
    ↓
Service (app/services/cart_service.py)  → "Business logic: can we add this?"
    ↓
Repository (app/repositories/cart_repository.py) → "Talk to the database"
    ↓
Models (app/models/cart.py, cartItem.py) → "Database table structure"
    ↓
Database (PostgreSQL)
```

Each layer has ONE job. Let's go through them all.

---

## 1. Models — What the database tables look like

### Cart Model (`app/models/cart.py`)

```python
class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
```

**What this means:**
- Each row in the `cart` table represents ONE user's cart
- `user_id` has `unique=True` — this means each user can only have ONE cart (not 5 carts, just 1)
- `ForeignKey("users.id")` — this links to the `users` table. The database won't allow a `user_id` that doesn't exist in `users`
- Think of it like: "User #3 has Cart #7"

**Example data in the cart table:**
```
| id | user_id | created_at          |
|----|---------|---------------------|
| 1  | 3       | 2026-06-24 10:00:00 |
| 2  | 7       | 2026-06-24 11:30:00 |
```

### CartItem Model (`app/models/cartItem.py`)

```python
class CartItem(Base):
    __tablename__ = "cart_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

**What this means:**
- Each row represents ONE product in a cart
- `cart_id` → links to which cart this item belongs to
- `product_id` → links to which product this is
- `quantity` → how many of this product the user wants
- NO `unique=True` on `cart_id` — because a cart can have MANY items

**Example data in the cart_item table:**
```
| id | cart_id | product_id | quantity | added_at            |
|----|---------|------------|----------|---------------------|
| 1  | 1       | 5          | 2        | 2026-06-24 10:05:00 |
| 2  | 1       | 8          | 1        | 2026-06-24 10:06:00 |
| 3  | 2       | 5          | 3        | 2026-06-24 11:35:00 |
```

Reading this: Cart #1 (belonging to User #3) has 2 items — 2x Product #5 and 1x Product #8.

### How Models connect:
```
users table          cart table           cart_item table        product table
+----+------+       +----+---------+     +----+---------+-----+  +----+--------+
| id | name |  ←──  | id | user_id |  ←──| id | cart_id | qty |  | id | name   |
+----+------+       +----+---------+     +----+---------+-----+  +----+--------+
| 3  | Ali  |       | 1  | 3       |     | 1  | 1       | 2   |──→ 5  | Phone  |
| 7  | Sara |       | 2  | 7       |     | 2  | 1       | 1   |──→ 8  | Laptop |
+----+------+       +----+---------+     +----+---------+-----+  +----+--------+
                         ↑                     ↑
                    ForeignKey            ForeignKey
                    (one user =           (one cart =
                     one cart)             many items)
```

---

## 2. Schemas — Validating what the user sends and what we return

### AddCartItem (Request Schema)

```python
class AddCartItem(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v
```

**What this means:**
- When a user sends a request, FastAPI uses this schema to validate the JSON body
- `product_id: int` — must be an integer, if user sends "abc" → automatic 422 error
- `quantity: int` — must be an integer
- `@field_validator("quantity")` — a custom rule: if quantity is 0 or negative, reject with 422
- This runs BEFORE any of our code. FastAPI handles the validation automatically

**Example — what happens with different inputs:**
```
{"product_id": 5, "quantity": 2}    → Valid, passes through
{"product_id": 5, "quantity": 0}    → 422 "Quantity must be greater than 0"
{"product_id": 5, "quantity": -1}   → 422 "Quantity must be greater than 0"
{"product_id": 5}                   → 422 "quantity field required"
{"quantity": 2}                     → 422 "product_id field required"
```

### CartItemResponse (Response Schema)

```python
class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**What this means:**
- This defines what the API returns to the user after adding an item
- `model_config = ConfigDict(from_attributes=True)` — this tells Pydantic: "you'll receive a SQLAlchemy object (like CartItem), read its attributes directly". Without this, Pydantic can't convert the database object to JSON.

**Example response the user sees:**
```json
{
    "id": 1,
    "cart_id": 1,
    "product_id": 5,
    "quantity": 2,
    "added_at": "2026-06-24T10:05:00"
}
```

---

## 3. Route — The entry point for the request

```python
router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(
    data: AddCartItem,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return cart_service.add_item_to_cart(db, current_user.id, data)
```

**Line by line:**

- `@router.post("/items", ...)` — this creates the endpoint `POST /cart/items` (prefix "/cart" + "/items")
- `response_model=CartItemResponse` — tells FastAPI: "format the response using this schema"
- `status_code=201` — return 201 (Created) on success, not the default 200
- `data: AddCartItem` — FastAPI reads the JSON body and validates it using the schema. If validation fails, it returns 422 automatically. Our code never runs.
- `current_user: User = Depends(get_current_user)` — this is the authentication. `get_current_user` reads the Bearer token, decodes it, finds the user. If no token → 401. This gives us the logged-in user object.
- `db: Session = Depends(get_db)` — gives us a database connection
- `cart_service.add_item_to_cart(db, current_user.id, data)` — passes three things to the service:
  1. `db` — the database connection
  2. `current_user.id` — WHO is adding (so we find their cart)
  3. `data` — WHAT they want to add (product_id + quantity)

**Why no admin check?** Unlike product/category routes, ANY authenticated user can add to cart. It's their own cart, not an admin operation.

**Why pass `current_user.id` not `current_user`?** The service only needs the user's ID to find their cart. It doesn't need the full user object. Keep it simple.

---

## 4. Repository — Talking to the database

The repository has 5 functions. Each one does ONE database operation.

### Function 1: Find a user's cart
```python
def get_cart_by_user_id(db: Session, user_id: int) -> Cart | None:
    statement = select(Cart).where(Cart.user_id == user_id)
    return db.execute(statement).scalars().first()
```
- SQL equivalent: `SELECT * FROM cart WHERE user_id = 3 LIMIT 1`
- Returns the Cart object if found, or `None` if the user has no cart yet

### Function 2: Create a new cart
```python
def create_cart(db: Session, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    db.add(cart)        # stage it
    db.commit()         # save to database
    db.refresh(cart)    # reload to get the auto-generated id
    return cart
```
- Creates a new cart for a first-time user
- `db.add()` → tells SQLAlchemy "I want to insert this"
- `db.commit()` → actually writes it to the database
- `db.refresh()` → reloads the object so `cart.id` has the auto-generated value

### Function 3: Check if a product is already in the cart
```python
def get_cart_item(db: Session, cart_id: int, product_id: int) -> CartItem | None:
    statement = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id,
    )
    return db.execute(statement).scalars().first()
```
- SQL equivalent: `SELECT * FROM cart_item WHERE cart_id = 1 AND product_id = 5 LIMIT 1`
- Two conditions: matches BOTH the cart AND the product
- Returns the CartItem if found (product already in cart), or `None` (product not in cart yet)

### Function 4: Add a new item to cart
```python
def add_cart_item(db: Session, cart_item: CartItem) -> CartItem:
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item
```
- Inserts a new row into `cart_item` table
- Used when the product is NOT already in the cart

### Function 5: Update quantity of existing item
```python
def update_cart_item_quantity(db: Session, cart_item: CartItem, quantity: int) -> CartItem:
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item
```
- Changes the quantity of an existing cart item
- Used when the product IS already in the cart (e.g., user adds 2 more phones when they already have 1)
- SQLAlchemy tracks changes — when you modify `cart_item.quantity` and call `commit()`, it generates: `UPDATE cart_item SET quantity = 3 WHERE id = 1`

---

## 5. Service — The business logic (the brain)

This is where all the decision-making happens.

```python
def add_item_to_cart(db: Session, user_id: int, data: AddCartItem):
```
Takes the database connection, user's ID, and validated request data.

### Step 1: Check if product exists
```python
    product = product_repository.get_by_id(db, data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
```
- Calls the PRODUCT repository (not cart!) to check if the product exists
- `get_by_id` already filters `is_active == True`, so deleted products return None
- If product doesn't exist → 404 error, execution STOPS here

### Step 2: Check available stock
```python
    inventory = inventory_repository.get_by_product_id(db, data.product_id)
    available_stock = inventory.stock_quantity if inventory else 0
```
- Calls the INVENTORY repository to see how many units are in stock
- If no inventory record exists, treat stock as 0
- We don't check stock here yet — we just get the number for later

### Step 3: Get or create the user's cart
```python
    cart = cart_repository.get_cart_by_user_id(db, user_id)
    if not cart:
        cart = cart_repository.create_cart(db, user_id)
```
- First time a user adds something? They don't have a cart yet
- `get_cart_by_user_id` returns `None` → we create one
- Second time? `get_cart_by_user_id` finds their existing cart → we reuse it
- This is the "get or create" pattern — very common

### Step 4: Check if product is already in cart
```python
    existing_item = cart_repository.get_cart_item(db, cart.id, data.product_id)
```
- Looks for this specific product in this specific cart
- This determines which path we take next

### Path A: Product already in cart → increase quantity
```python
    if existing_item:
        new_quantity = existing_item.quantity + data.quantity
        if new_quantity > available_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock"
            )
        return cart_repository.update_cart_item_quantity(db, existing_item, new_quantity)
```
- Example: User already has 2 phones in cart, now adds 3 more → `new_quantity = 2 + 3 = 5`
- Check: do we have 5 phones in stock? If only 4 → 409 error
- If stock is sufficient → update the existing cart item's quantity to 5
- Returns the updated cart item

### Path B: Product NOT in cart → add new item
```python
    else:
        if data.quantity > available_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock"
            )
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        return cart_repository.add_cart_item(db, cart_item)
```
- Example: User wants 2 phones, has none in cart yet
- Check: do we have 2 phones in stock? If only 1 → 409 error
- If sufficient → create a new CartItem and save it
- Returns the new cart item

---

## Complete Flow Example

**Scenario:** User Ali (id=3) sends `POST /cart/items` with `{"product_id": 5, "quantity": 2}`

```
1. ROUTE receives request
   ├── FastAPI validates body with AddCartItem schema ✓
   ├── get_current_user decodes token → Ali (id=3) ✓
   └── Calls: cart_service.add_item_to_cart(db, 3, data)

2. SERVICE starts
   ├── Step 1: product_repository.get_by_id(db, 5)
   │   └── Found! Product "Phone" exists and is active ✓
   │
   ├── Step 2: inventory_repository.get_by_product_id(db, 5)
   │   └── Found! stock_quantity = 10 → available_stock = 10
   │
   ├── Step 3: cart_repository.get_cart_by_user_id(db, 3)
   │   └── None! Ali has no cart → create_cart(db, 3) → Cart(id=1)
   │
   ├── Step 4: cart_repository.get_cart_item(db, 1, 5)
   │   └── None! Phone not in cart yet
   │
   └── Path B: 2 <= 10? Yes! → add_cart_item(db, CartItem(cart_id=1, product_id=5, quantity=2))

3. RESPONSE returned:
   {
       "id": 1,
       "cart_id": 1,
       "product_id": 5,
       "quantity": 2,
       "added_at": "2026-06-24T10:05:00"
   }
```

**Now Ali adds 3 MORE phones:**

```
1. ROUTE → same flow, calls service

2. SERVICE starts
   ├── Step 1: Product "Phone" exists ✓
   ├── Step 2: available_stock = 10
   ├── Step 3: Cart(id=1) found! (already exists from before)
   ├── Step 4: CartItem found! (quantity=2, the one from before)
   │
   └── Path A: new_quantity = 2 + 3 = 5. Is 5 <= 10? Yes!
       → update_cart_item_quantity(db, existing_item, 5)

3. RESPONSE:
   {
       "id": 1,
       "cart_id": 1,
       "product_id": 5,
       "quantity": 5,      ← updated from 2 to 5
       "added_at": "2026-06-24T10:05:00"
   }
```

---

## Error Cases Summary

| Situation | What catches it | Error |
|-----------|----------------|-------|
| No auth token | `get_current_user` in route | 401 |
| quantity = 0 or -1 | `@field_validator` in schema | 422 |
| missing product_id | Pydantic schema validation | 422 |
| product doesn't exist | Service Step 1 | 404 |
| product is deleted (is_active=False) | Service Step 1 (get_by_id filters) | 404 |
| not enough stock (new item) | Service Path B | 409 |
| not enough stock (existing + new) | Service Path A | 409 |

---

## How the files connect to each other

```
app/api/cart.py
    imports → app/schemas/cart.py         (AddCartItem, CartItemResponse)
    imports → app/services/cart_service.py (add_item_to_cart function)
    imports → app/dependencies/auth.py    (get_current_user)

app/services/cart_service.py
    imports → app/repositories/cart_repository.py      (cart DB operations)
    imports → app/repositories/product_repository.py   (check product exists)
    imports → app/repositories/inventory_repository.py (check stock)
    imports → app/models/cartItem.py                   (to create CartItem objects)

app/repositories/cart_repository.py
    imports → app/models/cart.py      (Cart model for queries)
    imports → app/models/cartItem.py  (CartItem model for queries)

app/main.py
    imports → app/api/cart.py (registers the router so FastAPI knows about /cart/items)

alembic/env.py
    imports → app/models/cart.py, cartItem.py (so Alembic can create the tables)
```
