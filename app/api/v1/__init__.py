"""Endpoints"""

from fastapi import APIRouter

from app.api.v1.generate_section import router_generate_secion
from app.api.v1.history import router_history


router_v1 = APIRouter(prefix = "/v1")
router_v1.include_router(router_generate_secion)
router_v1.include_router(router_history)
