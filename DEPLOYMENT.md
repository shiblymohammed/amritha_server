# Heritage Hotel Backend - Render Deployment Guide

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Cloudinary Account**: For image storage
4. **Gmail App Password**: For email functionality

## Deployment Steps

### 1. Database Setup
1. In Render Dashboard, create a new **PostgreSQL** database
2. Note down the database connection details

### 2. Web Service Setup
1. Create a new **Web Service** in Render
2. Connect your GitHub repository
3. Set the following configuration:
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn core.wsgi:application`
   - **Root Directory**: `server` (if your Django app is in a subdirectory)

### 3. Environment Variables
Set these environment variables in Render:

#### Required Variables:
```
SECRET_KEY=<generate-a-secure-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-render-app-url>.onrender.com
DATABASE_NAME=<your-database-name>
DATABASE_USER=<your-database-user>
DATABASE_PASSWORD=<your-database-password>
DATABASE_HOST=<your-database-host>
DATABASE_PORT=5432
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=<your-frontend-urls-comma-separated>
```

#### Cloudinary Variables:
```
CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
CLOUDINARY_API_KEY=<your-cloudinary-api-key>
CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
```

#### Email Variables:
```
EMAIL_HOST_USER=<your-gmail-address>
EMAIL_HOST_PASSWORD=<your-gmail-app-password>
DEFAULT_FROM_EMAIL=Heritage Hotel <your-gmail-address>
ADMIN_EMAIL=<admin-email-address>
```

### 4. Frontend Configuration
Update your frontend API base URL to point to your Render backend:
```
https://<your-render-app-name>.onrender.com/api/
```

### 5. Post-Deployment
1. Your app will automatically run migrations during build
2. Create a superuser (if needed):
   ```bash
   python manage.py createsuperuser
   ```
3. Test all API endpoints
4. Verify email functionality

## Important Notes

- **Free Tier Limitations**: Render free tier spins down after 15 minutes of inactivity
- **Cold Starts**: First request after spin-down may take 30-60 seconds
- **Database**: PostgreSQL database is required for production
- **Static Files**: Handled by WhiteNoise middleware
- **Media Files**: Stored in Cloudinary (not local filesystem)

## Troubleshooting

### Common Issues:
1. **Build Failures**: Check build logs for missing dependencies
2. **Database Connection**: Verify database environment variables
3. **CORS Errors**: Update CORS_ALLOWED_ORIGINS with your frontend URLs
4. **Static Files**: Ensure WhiteNoise is properly configured

### Logs:
- View logs in Render Dashboard under your service
- Use `python manage.py check --deploy` for deployment checks

## Local Development with Production Settings

To test production settings locally:
1. Copy `.env.example` to `.env`
2. Set `USE_SQLITE=True` for local database
3. Set `DEBUG=True` for development
4. Update other variables as needed

## Security Checklist

- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS properly configured
- [ ] CORS_ALLOW_ALL_ORIGINS=False
- [ ] Database credentials are secure
- [ ] Email credentials are app passwords (not account passwords)
- [ ] Cloudinary credentials are secure