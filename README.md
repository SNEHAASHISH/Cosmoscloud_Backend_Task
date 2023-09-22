# E-commerce API with FastAPI and MongoDB

This project is an example backend application for an e-commerce platform. It uses FastAPI as the web framework and MongoDB for storage. The application provides various API endpoints to manage products and orders.

## File Structure

- `main.py`: The main application file that contains all the API endpoints, models, and database connection details.

## Application Structure

### Models

1. `Product`: Represents a product in the e-commerce platform.
   - Attributes: `id`, `name`, `price`, `available_quantity`
2. `UserAddress`: Represents the shipping address of a user.
   - Attributes: `city`, `country`, `zip_code`
3. `OrderItem`: Represents an item in an order.
   - Attributes: `product_id`, `bought_quantity`
4. `Order`: Represents an order placed by a user.
   - Attributes: `timestamp`, `items`, `total_amount`, `user_address`

### API Endpoints

1. `GET /`: A welcome endpoint.
2. `GET /products/`: Lists all available products.
3. `POST /orders/`: Creates a new order.
4. `GET /orders/`: Lists all orders with optional pagination.
5. `GET /orders/{order_id}`: Fetches details of a specific order.
6. `PATCH /products/{product_id}`: Updates the available quantity of a specific product.

### Database

The application uses MongoDB as its database. The MongoDB connection is established using the `motor` asynchronous driver. The connection details are defined at the beginning of `main.py`.

### Mock Data

The application starts with mock data for products defined in the `products_db` list. The `orders_db` list will store orders as they're created via the API.

## Running the Application

1. Install the necessary packages:

```bash
pip install fastapi[all] motor uvicorn
```

2. Run the FastAPI application:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000/`.

## Testing

You can test the API using tools like Postman or directly through the Swagger UI at `http://127.0.0.1:8000/docs`.
