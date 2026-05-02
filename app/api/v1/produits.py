from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.produit import Produit
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate, StockOperation
from app.services.cloudinary_service import upload_image
from app.services.produit_service import (
    create_produit,
    decrement_stock,
    delete_produit,
    get_produit_or_404,
    increment_stock,
    update_produit,
)


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "",
    response_model=ProduitRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau produit avec upload Cloudinary",
)
def create(
    libelle: str = Form(..., examples=["Riz parfumé"]),
    prix_unitaire: Decimal = Form(..., gt=0, examples=["12000.00"]),
    quantite_stock: int = Form(0, ge=0, examples=[10]),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Produit:
    image_url = upload_image(image)
    payload = ProduitCreate(
        libelle=libelle,
        prix_unitaire=prix_unitaire,
        quantite_stock=quantite_stock,
        image_url=image_url,
    )
    return create_produit(db, payload)


@router.get("", response_model=list[ProduitRead], summary="Lister les produits")
def list_all(
    db: Session = Depends(get_db),
) -> list[Produit]:
    return db.query(Produit).order_by(Produit.id.desc()).all()


@router.get(
    "/{produit_id}",
    response_model=ProduitRead,
    summary="Afficher un produit par son identifiant",
)
def retrieve(
    produit_id: int,
    db: Session = Depends(get_db),
) -> Produit:
    return get_produit_or_404(db, produit_id)


@router.put(
    "/{produit_id}",
    response_model=ProduitRead,
    summary="Modifier un produit",
)
def update(
    produit_id: int,
    libelle: str | None = Form(default=None),
    prix_unitaire: Decimal | None = Form(default=None, gt=0),
    quantite_stock: int | None = Form(default=None, ge=0),
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
) -> Produit:
    image_url = upload_image(image) if image is not None else None
    payload = ProduitUpdate(
        libelle=libelle,
        prix_unitaire=prix_unitaire,
        quantite_stock=quantite_stock,
        image_url=image_url,
    )
    return update_produit(db, produit_id, payload)


@router.delete(
    "/{produit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un produit",
)
def delete(
    produit_id: int,
    db: Session = Depends(get_db),
) -> Response:
    delete_produit(db, produit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{produit_id}/increment",
    response_model=ProduitRead,
    summary="Incrémenter la quantité en stock",
)
def increment(
    produit_id: int,
    payload: StockOperation,
    db: Session = Depends(get_db),
) -> Produit:
    return increment_stock(db, produit_id, payload.quantite)


@router.patch(
    "/{produit_id}/decrement",
    response_model=ProduitRead,
    summary="Décrémenter la quantité en stock",
)
def decrement(
    produit_id: int,
    payload: StockOperation,
    db: Session = Depends(get_db),
) -> Produit:
    return decrement_stock(db, produit_id, payload.quantite)
