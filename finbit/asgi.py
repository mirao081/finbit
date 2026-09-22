"""
ASGI config for finbit project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

importos

fromdjango.core.asgiimportget_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE','finbit.settings')

application=get_asgi_application()
