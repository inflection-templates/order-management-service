from .otp import Otp
from .user_login_session import UserLoginSession

# Import User from parent user.py file to support imports like "from app.database.models.user import User"
import importlib.util
from pathlib import Path
_parent_dir = Path(__file__).parent.parent
_user_file_path = _parent_dir / "user.py"
_user_spec = importlib.util.spec_from_file_location("_user_module", _user_file_path)
_user_module = importlib.util.module_from_spec(_user_spec)
_user_spec.loader.exec_module(_user_module)
User = _user_module.User

__all__ = ['Otp', 'UserLoginSession', 'User']

