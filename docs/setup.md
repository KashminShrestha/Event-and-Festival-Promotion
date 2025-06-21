# 📦 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/event-festival-promotion.git
```

```bash
cd event-festival-promotion
```

### Create and activate a virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configure your environment variables (see below)

### Run migrations

```bash
python manage.py migrate
```

### Start the development server

```bash
python manage.py runserver
```

## Environment Variables Example (`.env`)

> 💡 **Tip:** Use a `.env` file to manage environment variables securely.

```bash
DEBUG=True

# ==============================
# 🔥 Firebase Configuration
# ==============================
FIREBASE_API_KEY="your-firebase-api-key"
FIREBASE_AUTH_DOMAIN="your-firebase-auth-domain"
FIREBASE_DATABASE_URL="your-firebase-db-url"
FIREBASE_PROJECT_ID="your-firebase-project-id"
FIREBASE_STORAGE_BUCKET="your-firebase-storage-bucket"
FIREBASE_MESSAGING_SENDER_ID="your-messaging-sender-id"
FIREBASE_APP_ID="your-firebase-app-id"
FIREBASE_MEASUREMENT_ID="your-measurement-id"
FIREBASE_CREDENTIAL_PATH="firebase_key.json"  # Path to your Firebase service account key

# ==============================
# 💳 Khalti Payment Gateway
# ==============================
KHALTI_VERIFY_URL="https://khalti.com/api/v2/payment/verify/"
KHALTI_PUBLIC_KEY="your-khalti-public-key"
KHALTI_SECRET_KEY="your-khalti-secret-key"

# ==============================
# 📧 Email Configuration (MailHog)
# ==============================

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST="your-mailhog-host"
EMAIL_PORT="your-mailhog-port"
EMAIL_USE_TLS=False
EMAIL_USE_SSL=False
EMAIL_HOST_USER="your-mailhog-username"
EMAIL_HOST_PASSWORD="your-mailhog-password"
DEFAULT_FROM_EMAIL=noreply@example.com

# ==============================
# 📧 Email Configuration (Mailtrap)
# ==============================
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="sandbox.smtp.mailtrap.io"
EMAIL_PORT=465
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-mailtrap-username"
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL="noreply@example.com"
```

> 📒 **Note:** Debug mode (True for development, False for production)
> & Replace all placeholder values with your actual credentials before running the project.

> ⚠️ **Warning:** This should not be pushed into git.

> 🟥 **Note:** Skip Docker and Mailhog installation if you use Mailtrap in
> Configuraion and use appropriate setup in settings.py

### 🐳 Using Docker for MailHog (Email Testing)

You can use MailHog to capture and view emails sent from the application during development. MailHog runs easily in Docker and provides a web interface for viewing emails.

Start MailHog in Docker

```bash
docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

- SMTP server: localhost:1025

- Web UI: http://localhost:8025

### Stop MailHog after testing

```bash
docker stop mailhog
docker rm mailhog
```

---

