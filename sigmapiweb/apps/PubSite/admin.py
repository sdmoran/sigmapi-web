"""
Admin config for PubSite app.
"""
from common.utils import register_model_admins

from .models import ArticleBlock


register_model_admins(ArticleBlock)
