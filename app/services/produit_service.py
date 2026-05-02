from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.produit import Produit
from app.schemas.produit import ProduitCreate, ProduitUpdate


def get_produit_or_404(db: Session, produit_id: int) -> Produit:
    produit = db.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable",
        )
    return produit


def create_produit(db: Session, payload: ProduitCreate) -> Produit:
    produit = Produit(**payload.model_dump())
    db.add(produit)
    db.commit()
    db.refresh(produit)
    return produit


def update_produit(db: Session, produit_id: int, payload: ProduitUpdate) -> Produit:
    produit = get_produit_or_404(db, produit_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(produit, field, value)
    db.commit()
    db.refresh(produit)
    return produit


def delete_produit(db: Session, produit_id: int) -> None:
    produit = get_produit_or_404(db, produit_id)
    db.delete(produit)
    db.commit()


def increment_stock(db: Session, produit_id: int, quantite: int) -> Produit:
    produit = get_produit_or_404(db, produit_id)
    produit.quantite_stock += quantite
    db.commit()
    db.refresh(produit)
    return produit


def decrement_stock(db: Session, produit_id: int, quantite: int) -> Produit:
    produit = get_produit_or_404(db, produit_id)
    if quantite > produit.quantite_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock insuffisant: la quantité en stock ne peut pas être négative",
        )
    produit.quantite_stock -= quantite
    db.commit()
    db.refresh(produit)
    return produit
