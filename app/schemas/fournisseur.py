from pydantic import BaseModel, Field


class FournisseurBase(BaseModel):
    nom: str = Field(min_length=2, max_length=150, examples=["SEN Fournitures"])
    telephone: str = Field(min_length=5, max_length=30, examples=["771234567"])
    adresse: str = Field(min_length=2, max_length=255, examples=["Dakar, Plateau"])


class FournisseurCreate(FournisseurBase):
    pass


class FournisseurUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    telephone: str | None = Field(default=None, min_length=5, max_length=30)
    adresse: str | None = Field(default=None, min_length=2, max_length=255)


class FournisseurRead(FournisseurBase):
    id: int

    model_config = {"from_attributes": True}
