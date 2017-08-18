"""
Admin config for Links app.
"""
from common.utils import register_model_admins

from .models import Link


register_model_admins(
    Link,
)
