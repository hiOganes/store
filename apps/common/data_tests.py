test_user_register = {
    'username': 'Test',
    'email': 'test@test.com',
    'password': '12345',
}

test_admin_user_register = {
    'username': 'Test_admin',
    'email': 'admin@admin.com',
    'password': '12345',
    'is_staff': True,
}

test_other_user_register = {
    'username': 'Otheruser',
    'email': 'other@user.com',
    'password': 'otherpass',
}

test_user_login = {
    'email': 'test@test.com',
    'password': '12345',
}

test_admin_user_login = {
    'email': 'admin@admin.com',
    'password': '12345',
}

test_user_login_ivalid_data = {
    'email': 'doesnot@exist.com',
    'password': '12345',
}

test_products = {
        "name": "Test",
        "description": "Test description",
        "price": 1,
        "stock": 5,
        "category": "electronics"
    }

test_products2 = {
        "name": "Test2",
        "description": "Test description2",
        "price": 2,
        "stock": 5,
        "category": "books"
    }

test_order = {
  'products': [
    1, 2
  ]
}