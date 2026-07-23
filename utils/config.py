import json

SLOW_MO = 1000

A_TO_Z = "Name (A to Z)"
Z_TO_A = "Name (Z to A)"
PRICE_HIGH_TO_LOW = "Price (low to high)"
PRICE_LOW_TO_HIGH = "Price (high to low)"

# SORT_BY = [A_TO_Z]
SORT_BY = [A_TO_Z, Z_TO_A, PRICE_HIGH_TO_LOW, PRICE_LOW_TO_HIGH]

USERS = [
    ("standard_user", "secret_sauce", "inventory.html"),
    ("locked_out_user", "secret_sauce", " Sorry, this user has been locked out."),
    ("problem_user", "secret_sauce", "inventory.html"),
    ("performance_glitch_user", "secret_sauce", "inventory.html"),
    ("error_user", "secret_sauce", "inventory.html"),
    ("visual_user", "secret_sauce", "inventory.html"),
]

LOGIN_SCENARIOS =[
        ("", "", "Username is required"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("invalid_user", "secret_sauce", "Username and password"),
        ("standard_user", "invalid_password",
         " Username and password do not match any user in this service"),
        ("invalid_user", "invalid_password",
         " Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
        ("standard_user", "secret_sauce", "inventory.html"),
    ]

CHECKOUT_INFO = [
    ("", "", "", "First Name is required"),
    ("Narsimha", "", "", "Last Name is required"),
    ("Narsimha", "Akula", "", "Postal Code is required"),
    ("Narsimha", "Akula", "500056", "checkout-step-two.html"),
]

with open("configs/config.json") as f:
    config = json.load(f)

def get(key):
    return config.get(key)

def get_web_elements(key):
    return config['web_elements'].get(key)

def get_login_elements(key):
    return config["web_elements"]["login_page"].get(key)

def get_inventory_elements(key):
    return config["web_elements"]["inventory_page"].get(key)

def get_product_elements(key):
    return config["web_elements"]["product_page"].get(key)

def get_footer_elements(key):
    return config["web_elements"]["footer"].get(key)

def get_checkout_elements(key):
    return config["web_elements"]["checkout"].get(key)


