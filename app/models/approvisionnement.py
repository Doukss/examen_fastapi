from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Approvisionnement(Base):
    __tablename__ = "approvisionnements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    quantite: Mapped[int] = mapped_column(Integer, nullable=False)
    fournisseur_id: Mapped[int] = mapped_column(ForeignKey("fournisseurs.id"), nullable=False)
    produit_id: Mapped[int] = mapped_column(ForeignKey("produits.id"), nullable=False)

    fournisseur = relationship("Fournisseur", back_populates="approvisionnements")
    produit = relationship("Produit", back_populates="approvisionnements")
