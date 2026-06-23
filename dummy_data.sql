INSERT INTO category (name, description, is_active) VALUES
('Electronics',    'Phones, laptops, and gadgets',          true),
('Clothing',       'Men and women apparel',                 true),
('Books',          'Fiction, non-fiction, and textbooks',    true),
('Home & Kitchen', 'Furniture, appliances, and cookware',   true),
('Sports',         'Gym equipment and outdoor gear',        true);

INSERT INTO product (name, description, price, category_id, is_active) VALUES
('iPhone 15',           'Latest Apple smartphone',           999.99,  1, true),
('Samsung Galaxy S24',  'Android flagship phone',            899.99,  1, true),
('MacBook Pro 16',      'Apple laptop for professionals',    2499.99, 1, true),
('AirPods Pro',         'Wireless noise-cancelling earbuds', 249.99,  1, true),
('Dell Monitor 27"',    '4K Ultra HD monitor',               349.99,  1, true),
('Nike T-Shirt',        'Cotton casual t-shirt',             29.99,   2, true),
('Levi Jeans',          'Classic blue denim jeans',          59.99,   2, true),
('Adidas Hoodie',       'Warm fleece hoodie',                49.99,   2, true),
('Python Crash Course', 'Learn Python programming',          39.99,   3, true),
('Clean Code',          'Software craftsmanship guide',      44.99,   3, true),
('The Pragmatic Programmer', 'Tips for better coding',       49.99,   3, true),
('Air Fryer',           'Digital air fryer 5L',              89.99,   4, true),
('Blender Pro',         'High-speed blender 1000W',          69.99,   4, true),
('Yoga Mat',            'Non-slip exercise mat',             24.99,   5, true),
('Dumbbell Set',        '10kg adjustable dumbbells',         79.99,   5, true);

INSERT INTO inventory (product_id, stock_quantity) VALUES
(1, 50), (2, 35), (3, 20), (4, 100), (5, 40),
(6, 200), (7, 150), (8, 120), (9, 75), (10, 60),
(11, 45), (12, 80), (13, 65), (14, 90), (15, 55);
