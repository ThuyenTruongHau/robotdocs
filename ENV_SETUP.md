# Environment Setup Guide

## 🚀 For Local Development

### 1. Generate .env file
```bash
python setup_env.py
```

### 2. Update database settings in .env
```env
DB_NAME=thado_robot
DB_USER=postgres
DB_PASSWORD=your-local-password
DB_HOST=localhost
DB_PORT=5432
```

## 🌐 For Render Deployment

### Environment Variables to set in Render:

#### Required Variables:
```
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=rfid.thadorobot.com,your-app.onrender.com
```

#### Database Variables:
```
DB_NAME=thado_robot
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=your-postgres-host
DB_PORT=5432
```

#### Optional Variables:
```
JWT_SECRET_KEY=your-jwt-secret
API_KEY=your-api-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
REDIS_URL=redis://your-redis-host:6379/0
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0
```

## 🔧 How to set Environment Variables in Render:

1. Go to your Render dashboard
2. Select your Web Service
3. Go to "Environment" tab
4. Add each variable with its value
5. Click "Save Changes"
6. Redeploy your service

## ⚠️ Important Notes:

- Never commit `.env` file to git (it's in .gitignore)
- Use strong, unique SECRET_KEY for production
- Database credentials should match your Render PostgreSQL database
- ALLOWED_HOSTS should include your Render app URL
