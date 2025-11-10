# 🚀 Deploying to Render

This guide will help you deploy your Dairy Farm Management System (CowConnect) to Render.

## Prerequisites
- GitHub account with your code pushed to repository
- Render account (free tier available at https://render.com)

## Step-by-Step Deployment

### 1. Create a New Web Service on Render

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `https://github.com/rohitbaba001/Cow`
4. Configure the service:

### 2. Service Configuration

**Basic Settings:**
- **Name:** `cowconnect` (or your preferred name)
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn farm_management.wsgi:application`

### 3. Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | Generate a new secret key | Django secret key (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | `False` | Never set to True in production |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` | Your Render app URL |
| `PYTHON_VERSION` | `3.11.5` | Python version |

**Note:** Render automatically provides `DATABASE_URL` for PostgreSQL database.

### 4. Add PostgreSQL Database

1. In your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `cowconnect-db`
   - **Database:** `cowconnect`
   - **User:** `cowconnect_user`
   - **Region:** Same as your web service
   - **Plan:** Free
3. Click **"Create Database"**
4. Once created, go to your **Web Service** → **Environment** → Add:
   - Copy the **Internal Database URL** from your PostgreSQL instance
   - Add it as `DATABASE_URL` environment variable

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run `build.sh` (collectstatic & migrate)
   - Start the application with Gunicorn

### 6. Create Superuser

After deployment, you need to create an admin user:

1. Go to your service → **Shell** tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow the prompts to create your admin account

### 7. Access Your Application

Your app will be available at: `https://your-app-name.onrender.com`

## Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-50 seconds
- 750 hours/month free (enough for one service)

### Media Files
For production, consider using:
- **Cloudinary** for image storage
- **AWS S3** for file storage

### Database Backups
- Render Free PostgreSQL doesn't include automatic backups
- Consider upgrading to paid plan for production use

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `build.sh` has correct permissions
- Verify all dependencies in `requirements.txt`

### Static Files Not Loading
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Ensure `collectstatic` ran successfully
- Verify WhiteNoise is in MIDDLEWARE

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is set
- Check PostgreSQL instance is running
- Ensure database is in same region as web service

### Application Errors
- Check logs: Service → **Logs** tab
- Set `DEBUG=True` temporarily (remember to set back to False!)
- Verify all environment variables are set correctly

## Updating Your Application

To deploy updates:
1. Push changes to GitHub: `git push origin main`
2. Render automatically detects changes and redeploys
3. Monitor deployment in Render dashboard

## Security Checklist

- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` set
- ✅ `ALLOWED_HOSTS` configured correctly
- ✅ Database credentials secured
- ✅ `.gitignore` excludes sensitive files
- ✅ HTTPS enabled (automatic on Render)

## Cost Optimization

**Free Tier:**
- 1 Web Service (750 hours/month)
- 1 PostgreSQL Database (90 days, then expires)

**Upgrade Considerations:**
- Paid PostgreSQL for persistent data
- Faster instance types for better performance
- Custom domain support

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Community: https://community.render.com/

---

**Your app is now live! 🎉**

Access it at: `https://your-app-name.onrender.com`
