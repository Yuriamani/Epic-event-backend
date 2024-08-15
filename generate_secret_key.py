import secrets

# Generate app secret key
app_secret_key = secrets.token_hex(32)

# Generate JWT secret key
jwt_secret_key = secrets.token_urlsafe(16)

# Write both secret keys to .env file
with open('.env', 'a') as f:
    f.write(f"SECRET_KEY={app_secret_key}\n")
    f.write(f"JWT_SECRET_KEY={jwt_secret_key}\n")

print("Secret keys generated and written to .env file:")
print(f"SECRET_KEY={app_secret_key}")
print(f"JWT_SECRET_KEY={jwt_secret_key}")