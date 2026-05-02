from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.approvisionnement import Approvisionnement
from app.schemas.approvisionnement import (
    ApprovisionnementCreate,
    ApprovisionnementDetail,
    ApprovisionnementRead,
    ApprovisionnementUpdate,
)
from app.services.approvisionnement_service import (
    create_approvisionnement,
    delete_approvisionnement,
    get_approvisionnement_or_404,
    update_approvisionnement,
)


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "",
    response_model=ApprovisionnementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un approvisionnement et augmenter le stock",
)
def create(
    payload: ApprovisionnementCreate,
    db: Session = Depends(get_db),
) -> Approvisionnement:
    return create_approvisionnement(db, payload)


@router.get(
    "",
    response_model=list[ApprovisionnementDetail],
    summary="Lister les approvisionnements",
)
def list_all(db: Session = Depends(get_db)) -> list[Approvisionnement]:
    return (
        db.query(Approvisionnement)
        .options(
            joinedload(Approvisionnement.fournisseur),
            joinedload(Approvisionnement.produit),
        )
        .order_by(Approvisionnement.id.desc())
        .all()
    )


@router.get(
    "/{approvisionnement_id}",
    response_model=ApprovisionnementDetail,
    summary="Afficher un approvisionnement par son identifiant",
)
def retrieve(
    approvisionnement_id: int,
    db: Session = Depends(get_db),
) -> Approvisionnement:
    return get_approvisionnement_or_404(db, approvisionnement_id)


@router.put(
    "/{approvisionnement_id}",
    response_model=ApprovisionnementRead,
    summary="Modifier un approvisionnement",
)
def update(
    approvisionnement_id: int,
    payload: ApprovisionnementUpdate,
    db: Session = Depends(get_db),
) -> Approvisionnement:
    return update_approvisionnement(db, approvisionnement_id, payload)


@router.delete(
    "/{approvisionnement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un approvisionnement",
)
def delete(
    approvisionnement_id: int,
    db: Session = Depends(get_db),
) -> Response:
    delete_approvisionnement(db, approvisionnement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
