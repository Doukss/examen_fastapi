from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.fournisseur import Fournisseur
from app.schemas.fournisseur import (
    FournisseurCreate,
    FournisseurRead,
    FournisseurUpdate,
)
from app.services.fournisseur_service import (
    create_fournisseur,
    delete_fournisseur,
    get_fournisseur_or_404,
    update_fournisseur,
)


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "",
    response_model=FournisseurRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau fournisseur",
)
def create(
    payload: FournisseurCreate,
    db: Session = Depends(get_db),
) -> Fournisseur:
    return create_fournisseur(db, payload)


@router.get("", response_model=list[FournisseurRead], summary="Lister les fournisseurs")
def list_all(
    db: Session = Depends(get_db),
) -> list[Fournisseur]:
    return db.query(Fournisseur).order_by(Fournisseur.id.desc()).all()


@router.get(
    "/{fournisseur_id}",
    response_model=FournisseurRead,
    summary="Afficher un fournisseur par son identifiant",
)
def retrieve(
    fournisseur_id: int,
    db: Session = Depends(get_db),
) -> Fournisseur:
    return get_fournisseur_or_404(db, fournisseur_id)


@router.put(
    "/{fournisseur_id}",
    response_model=FournisseurRead,
    summary="Modifier un fournisseur",
)
def update(
    fournisseur_id: int,
    payload: FournisseurUpdate,
    db: Session = Depends(get_db),
) -> Fournisseur:
    return update_fournisseur(db, fournisseur_id, payload)


@router.delete(
    "/{fournisseur_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un fournisseur",
)
def delete(
    fournisseur_id: int,
    db: Session = Depends(get_db),
) -> Response:
    delete_fournisseur(db, fournisseur_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
