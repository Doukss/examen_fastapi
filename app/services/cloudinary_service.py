from fastapi import HTTPException, UploadFile, status
import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_image(file: UploadFile) -> str:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier envoyé doit être une image",
        )

    if not all(
        [
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configuration Cloudinary manquante",
        )

    result = cloudinary.uploader.upload(file.file, folder="examenfastapi/produits")
    return str(result["secure_url"])
