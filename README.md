# Ecommerce API

## Description

The Ecommerce API is a backend application designed to manage shopping carts and process checkouts. This API allows users to add items to their cart, calculate the total, and perform checkout. The goal is to provide an interface for creating and managing a simple and efficient shopping cart system.

## Models Created

### User

- **id**: Unique identifier for the user (integer, primary key).
- **username**: User's name (string).
- **email**: User's email address (string).
- **password**: User's password (string).
- **cart**: Relationship with items in the cart (one-to-many with `CartItem`).

### Product

- **id**: Unique identifier for the product (integer, primary key).
- **name**: Product name (string).
- **price**: Product price (decimal).

### CartItem

- **id**: Unique identifier for the cart item (integer, primary key).
- **user_id**: User identifier (integer, foreign key referencing `User`).
- **product_id**: Product identifier (integer, foreign key referencing `Product`).

## Features
```
    ### User

    - **Create User**: Allows for the creation of a new user account.
    - **Get User Details**: Retrieves the details of a user by ID.
    - **Update User Information**: Updates the user's information such as username, email, and password.
    - **Delete User**: Removes a user from the system.

    ### Product

    - **Create Product**: Adds a new product to the catalog.
    - **Get Product Details**: Retrieves details of a product by ID.
    - **Update Product Information**: Updates the product's name and price.
    - **Delete Product**: Removes a product from the catalog.

    ### Cart

    - **Add Item to Cart**: Allows users to add products to their cart.
    - **List Cart Items**: Displays items currently in a user's cart.
    - **Remove Item from Cart**: Removes a specific item from the cart.
    - **Checkout**: Calculates the total of the items in the cart and removes all items after payment.
```
## Usage Guide

1. **Installation and Usage**

   ```bash
   git clone https://github.com/malockey/ecommerce-api.git
   cd ecommerce-api
   pip install -r requirements.txt
   flask db upgrade
   flask run

2. **Swagger Installation in Postman**

To import the API documentation into Postman using the swagger.yaml file available in the repository:

    1. Open Postman and go to the "Import" tab in the top left corner.
    2. Select the "File" tab and click "Choose Files".
    3. Navigate to the swagger.yaml file in your repository and select it.
    4. Click "Open" to import the file.
    5. Postman will create a new collection with all the endpoints defined in the swagger.yaml.

3. **Testing the API**

Use the imported collection in Postman to test the API endpoints.