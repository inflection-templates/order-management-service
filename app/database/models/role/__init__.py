from .role_permissions import RolePermission
from .role_privileges import RolePrivilege

# Import Role from parent role.py file to support imports like "from app.database.models.role import Role"
import importlib.util
from pathlib import Path
_parent_dir = Path(__file__).parent.parent
_role_file_path = _parent_dir / "role.py"
_role_spec = importlib.util.spec_from_file_location("_role_module", _role_file_path)
_role_module = importlib.util.module_from_spec(_role_spec)
_role_spec.loader.exec_module(_role_module)
Role = _role_module.Role

__all__ = ['RolePermission', 'RolePrivilege', 'Role']

