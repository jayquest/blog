from django.utils.translation import gettext_noop
gettext_noop("AppName")

from django.conf import settings

settings.TEMPLATE_CONTEXT_PROCESSORS += ("blog.views.list_arquivo",)