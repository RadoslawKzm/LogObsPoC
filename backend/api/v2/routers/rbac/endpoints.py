import fastapi

from backend.api.v2.rbac.logic import require_role
from backend.api.v2.rbac.models import Role

rbac_router = fastapi.APIRouter(
    prefix="/rbac",
    tags=["rbac"],
)


@rbac_router.get("/admin-area")
def read_admin_area(user=fastapi.Depends(require_role(Role.ADMIN))):
    return {"message": f"Welcome admin {user.username}"}


@rbac_router.get("/shared-area")
def read_shared(user=fastapi.Depends(require_role(Role.ADMIN, Role.MANAGER))):
    return {"message": f"Welcome {user.role} {user.username}"}
