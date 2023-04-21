from src.apps import *

urlpatterns = [{"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]}]
