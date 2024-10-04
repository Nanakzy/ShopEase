import unittest
import json
from app import app

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.token = None

    def test_index_endpoint(self):
        print("Testing Index Endpoint")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_signup_new_user(self):
        print("Testing Signup New User")
        response = self.app.post('/signup', 
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "name": "Nana",
                                     "surname": "Dry",
                                     "password": "password",
                                     "confirm_password": "password"
                                 }), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print("Result:", response.data.decode())

    def test_signup_duplicate_user(self):
        print("Testing Signup Duplicate User")
        response = self.app.post('/signup', 
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "name": "Nana",
                                     "surname": "Dry",
                                     "password": "password",
                                     "confirm_password": "password"
                                 }), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_login(self):
        print("Testing Login")
        response = self.app.post('/login', 
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "password": "password"
                                 }), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.token = response.get_json().get('token')
        print("Result:", response.data.decode())

    def test_get_products(self):
        print("Testing Get Products Endpoint")
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_get_products_by_category(self):
        print("Testing Get Products By Category (Shoes)")
        response = self.app.get('/products?category=Shoes')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

        print("Testing Get Products By Category (Handbags)")
        response = self.app.get('/products?category=Handbags')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_add_product(self):
        print("Testing Add Product Endpoint")
        response = self.app.post('/admin/products',
                                 headers={"Authorization": f"Bearer {self.token}"},
                                 data=json.dumps({
                                     "name": "Product Name",
                                     "description": "Product Description",
                                     "price": 19.99,
                                     "image_url": "http://example.com/image.jpg",
                                     "category": "Shoes"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print("Result:", response.data.decode())

    def test_add_to_cart(self):
        print("Testing Add to Cart")
        response = self.app.post('/cart',
                                 headers={"Authorization": f"Bearer {self.token}"},
                                 data=json.dumps({
                                     "product_id": 1,
                                     "quantity": 2
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_checkout_session(self):
        print("Testing Checkout Session")
        response = self.app.post('/create-checkout-session',
                                 headers={"Authorization": f"Bearer {self.token}"},
                                 data=json.dumps({
                                     "product_name": "Sample Product",
                                     "amount": 2000,
                                     "quantity": 1
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_checkout_success(self):
        print("Testing Checkout Success")
        response = self.app.get('/success')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    def test_checkout_cancel(self):
        print("Testing Checkout Cancel")
        response = self.app.get('/cancel')
        self.assertEqual(response.status_code, 200)
        print("Result:", response.data.decode())

    # Error handling tests
    def test_signup_missing_fields(self):
        print("Testing Signup Missing Fields")
        response = self.app.post('/signup',
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "name": "Nana",
                                     "surname": "Dry"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_signup_password_mismatch(self):
        print("Testing Signup Password Mismatch")
        response = self.app.post('/signup',
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "name": "Nana",
                                     "surname": "Dry",
                                     "password": "password1",
                                     "confirm_password": "password2"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_login_invalid_email(self):
        print("Testing Login Invalid Email")
        response = self.app.post('/login',
                                 data=json.dumps({
                                     "email": "unknown@mymail.com",
                                     "password": "password"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_login_wrong_password(self):
        print("Testing Login Wrong Password")
        response = self.app.post('/login',
                                 data=json.dumps({
                                     "email": "nana@mymail.com",
                                     "password": "wrongpassword"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_get_products_invalid_category(self):
        print("Testing Get Products Invalid Category")
        response = self.app.get('/products?category=InvalidCategory')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_add_product_unauthorized(self):
        print("Testing Add Product Unauthorized Access")
        response = self.app.post('/admin/products',
                                 headers={"Authorization": "Bearer <INVALID_JWT_TOKEN>"},
                                 data=json.dumps({
                                     "name": "Product Name",
                                     "description": "Product Description",
                                     "price": 19.99,
                                     "image_url": "http://example.com/image.jpg",
                                     "category": "Shoes"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 403)
        print("Result:", response.data.decode())

    def test_add_product_missing_data(self):
        print("Testing Add Product Missing Data")
        response = self.app.post('/admin/products',
                                 headers={"Authorization": f"Bearer {self.token}"},
                                 data=json.dumps({
                                     "name": "",
                                     "description": "Product Description",
                                     "price": 19.99,
                                     "category": "Shoes"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_add_to_cart_invalid_product(self):
        print("Testing Add to Cart Invalid Product ID")
        response = self.app.post('/cart',
                                 headers={"Authorization": f"Bearer {self.token}"},
                                 data=json.dumps({
                                     "product_id": 9999,
                                     "quantity": 2
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
        print("Result:", response.data.decode())

    def test_checkout_session_missing_product_name(self):
        print("Testing Checkout Session Missing Product Name")
        response = self.app.post('/create-checkout-session',
                                 data=json.dumps({
                                     "amount": 2000,
                                     "quantity": 1
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

    def test_checkout_session_invalid_amount(self):
        print("Testing Checkout Session Invalid Amount")
        response = self.app.post('/create-checkout-session',
                                 data=json.dumps({
                                     "product_name": "Sample Product",
                                     "amount": -2000,
                                     "quantity": 1
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Result:", response.data.decode())

if __name__ == '__main__':
    unittest.main()

