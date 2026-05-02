from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ProduitBase(BaseModel):
    libelle: str = Field(min_length=2, max_length=150, examples=["Riz parfumé"])
    prix_unitaire: Decimal = Field(gt=0, examples=["12000.00"])
    quantite_stock: int = Field(default=0, ge=0, examples=[10])


class ProduitCreate(ProduitBase):
    image_url: str | None = None


class ProduitUpdate(BaseModel):
    libelle: str | None = Field(default=None, min_length=2, max_length=150)
    prix_unitaire: Decimal | None = Field(default=None, gt=0)
    quantite_stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None


class StockOperation(BaseModel):
    quantite: int = Field(gt=0, examples=[5])


class ProduitRead(ProduitBase):
    id: int
    image_url: str | None = None

    @field_validator("prix_unitaire")
    @classmethod
    def normalize_decimal(cls, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))

    model_config = {"from_attributes": True}
