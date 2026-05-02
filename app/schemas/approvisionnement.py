from datetime import date as date_type

from pydantic import BaseModel, Field

from app.schemas.fournisseur import FournisseurRead
from app.schemas.produit import ProduitRead


class ApprovisionnementBase(BaseModel):
    date: date_type = Field(examples=["2026-05-02"])
    quantite: int = Field(gt=0, examples=[20])
    fournisseur_id: int = Field(gt=0, examples=[1])
    produit_id: int = Field(gt=0, examples=[1])


class ApprovisionnementCreate(ApprovisionnementBase):
    pass


class ApprovisionnementUpdate(BaseModel):
    date: date_type | None = None
    quantite: int | None = Field(default=None, gt=0)
    fournisseur_id: int | None = Field(default=None, gt=0)
    produit_id: int | None = Field(default=None, gt=0)


class ApprovisionnementRead(ApprovisionnementBase):
    id: int

    model_config = {"from_attributes": True}


class ApprovisionnementDetail(ApprovisionnementRead):
    fournisseur: FournisseurRead
    produit: ProduitRead
