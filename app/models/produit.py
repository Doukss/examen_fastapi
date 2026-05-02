from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Produit(Base):
    __tablename__ = "produits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    libelle: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    prix_unitaire: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantite_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    approvisionnements = relationship(
        "Approvisionnement",
        back_populates="produit",
        cascade="all, delete-orphan",
    )
