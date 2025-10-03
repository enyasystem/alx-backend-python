Messaging app for Django-signals_orm-0x04 exercise

This small app provides a Message model and a Notification model.
A post_save signal on Message automatically creates a Notification for the receiving user.

To use:
- Add 'Django-signals_orm-0x04.messaging' to INSTALLED_APPS in your Django project settings.
- Run migrations: python manage.py makemigrations messaging && python manage.py migrate
- Create users and create Message objects; Notifications are created automatically.

Tests:
- The included tests use Django TestCase. Run them with:

    $ env DJANGO_SETTINGS_MODULE=your_project.settings python -m pytest Django-signals_orm-0x04/messaging/tests.py

Note: apps.py uses a try/except in ready() to avoid breaking project startup when Django isn't fully configured during static analysis.
