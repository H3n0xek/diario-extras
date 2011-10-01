from django.conf import settings

DIARIO_MAX_DRAFTS = getattr(settings, 'DIARIO_MAX_DRAFTS', 10)
DIARIO_LIMIT_DRAFTS = getattr(settings, 'DIARIO_LIMIT_DRAFTS', True)

