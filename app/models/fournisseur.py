from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Fournisseur(Base):
    __tablename__ = "fournisseurs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    telephone: Mapped[str] = mapped_column(String(30), nullable=False)
    adresse: Mapped[str] = mapped_column(String(255), nullable=False)

    approvisionnements = relationship(
        "Approvisionnement",
        back_populates="fournisseur",
        cascade="all, delete-orphan",
    )
