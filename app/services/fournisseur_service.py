from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.fournisseur import Fournisseur
from app.schemas.fournisseur import FournisseurCreate, FournisseurUpdate


def get_fournisseur_or_404(db: Session, fournisseur_id: int) -> Fournisseur:
    fournisseur = db.get(Fournisseur, fournisseur_id)
    if fournisseur is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fournisseur introuvable",
        )
    return fournisseur


def create_fournisseur(db: Session, payload: FournisseurCreate) -> Fournisseur:
    fournisseur = Fournisseur(**payload.model_dump())
    db.add(fournisseur)
    db.commit()
    db.refresh(fournisseur)
    return fournisseur


def update_fournisseur(
    db: Session, fournisseur_id: int, payload: FournisseurUpdate
) -> Fournisseur:
    fournisseur = get_fournisseur_or_404(db, fournisseur_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(fournisseur, field, value)
    db.commit()
    db.refresh(fournisseur)
    return fournisseur


def delete_fournisseur(db: Session, fournisseur_id: int) -> None:
    fournisseur = get_fournisseur_or_404(db, fournisseur_id)
    db.delete(fournisseur)
    db.commit()
