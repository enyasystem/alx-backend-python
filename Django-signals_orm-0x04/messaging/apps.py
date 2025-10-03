from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # The importable app name is the package folder 'messaging'
    name = 'messaging'

    def ready(self):
        # Import signal handlers to ensure they're connected
        try:
            from . import signals  # noqa: F401
        except Exception:
            # During test discovery or environments where Django isn't fully configured,
            # importing signals may fail; swallow exceptions to avoid breaking startup.
            pass
