from fastapi import APIRouter

from app.api.v1 import approvisionnements, auth, fournisseurs, produits


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(fournisseurs.router, prefix="/fournisseurs", tags=["Fournisseurs"])
api_router.include_router(produits.router, prefix="/produits", tags=["Produits"])
api_router.include_router(
    approvisionnements.router,
    prefix="/approvisionnements",
    tags=["Approvisionnements"],
)
