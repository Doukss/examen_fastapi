from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.approvisionnement import Approvisionnement
from app.schemas.approvisionnement import ApprovisionnementCreate, ApprovisionnementUpdate
from app.services.fournisseur_service import get_fournisseur_or_404
from app.services.produit_service import get_produit_or_404


def get_approvisionnement_or_404(
    db: Session, approvisionnement_id: int
) -> Approvisionnement:
    approvisionnement = db.get(Approvisionnement, approvisionnement_id)
    if approvisionnement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approvisionnement introuvable",
        )
    return approvisionnement


def create_approvisionnement(
    db: Session, payload: ApprovisionnementCreate
) -> Approvisionnement:
    get_fournisseur_or_404(db, payload.fournisseur_id)
    produit = get_produit_or_404(db, payload.produit_id)

    approvisionnement = Approvisionnement(**payload.model_dump())
    produit.quantite_stock += payload.quantite

    db.add(approvisionnement)
    db.commit()
    db.refresh(approvisionnement)
    return approvisionnement


def update_approvisionnement(
    db: Session,
    approvisionnement_id: int,
    payload: ApprovisionnementUpdate,
) -> Approvisionnement:
    approvisionnement = get_approvisionnement_or_404(db, approvisionnement_id)
    data = payload.model_dump(exclude_unset=True)

    if "fournisseur_id" in data:
        get_fournisseur_or_404(db, data["fournisseur_id"])
    if "produit_id" in data:
        get_produit_or_404(db, data["produit_id"])

    for field, value in data.items():
        setattr(approvisionnement, field, value)

    db.commit()
    db.refresh(approvisionnement)
    return approvisionnement


def delete_approvisionnement(db: Session, approvisionnement_id: int) -> None:
    approvisionnement = get_approvisionnement_or_404(db, approvisionnement_id)
    db.delete(approvisionnement)
    db.commit()
