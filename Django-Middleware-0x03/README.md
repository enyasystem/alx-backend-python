# Django-Middleware-0x03

This project is a copy of the messaging_app with custom middleware implementations for the milestone.

Added middleware in `chats/middleware.py`:
- `RequestLoggingMiddleware` — logs timestamp, user and path to `requests.log`.
- `RestrictAccessByTimeMiddleware` — blocks access outside 06:00-21:00.
- `OffensiveLanguageMiddleware` — rate-limits POST messages from an IP (5 per minute).
- `RolepermissionMiddleware` — requires admin/host roles for admin routes.

To run locally:

```powershell
cd Django-Middleware-0x03
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ../messaging_app/requirements.txt
python manage.py migrate
python manage.py runserver
```

Notes:
- Middleware is registered in `messaging_app/settings.py`.
- `requests.log` will be created in the project root when requests are made.
