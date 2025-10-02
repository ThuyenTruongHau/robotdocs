#!/usr/bin/env python3
"""
Script to generate .env file from env.template
"""

import os
import secrets
import string

def generate_secret_key():
    """Generate a secure Django secret key"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for _ in range(50))

def generate_jwt_secret():
    """Generate a secure JWT secret"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def setup_env():
    """Setup .env file from template"""
    template_file = 'env.template'
    env_file = '.env'
    
    if not os.path.exists(template_file):
        print(f"❌ Template file {template_file} not found!")
        return
    
    if os.path.exists(env_file):
        print(f"⚠️  {env_file} already exists. Backup created as {env_file}.backup")
        os.rename(env_file, f"{env_file}.backup")
    
    # Generate secrets
    secret_key = generate_secret_key()
    jwt_secret = generate_jwt_secret()
    
    # Read template
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace('your-secret-key-here-change-this-in-production', secret_key)
    content = content.replace('jwt-secret-key-here', jwt_secret)
    content = content.replace('your-app.onrender.com', 'your-app.onrender.com')
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"✅ {env_file} created successfully!")
    print(f"🔑 SECRET_KEY generated: {secret_key[:20]}...")
    print(f"🔑 JWT_SECRET generated: {jwt_secret[:10]}...")
    print("\n📋 Next steps:")
    print("1. Update database credentials in .env")
    print("2. Update email settings if needed")
    print("3. For Render deployment, set these as environment variables:")

if __name__ == "__main__":
    setup_env()
