# API RESTful de Gestion des Approvisionnements - FastAPI

Projet FastAPI avec PostgreSQL, SQLAlchemy, JWT, upload Cloudinary et documentation Swagger.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Créer la base PostgreSQL :

```sql
CREATE DATABASE examenfastapi;
```

Configurer les variables dans `.env`, puis lancer :

```bash
uvicorn app.main:app --reload
```

Documentation Swagger :

- `http://127.0.0.1:8000/api-docs`
- `http://127.0.0.1:8000/docs`

## Authentification

Toutes les routes métier sont protégées par JWT.

1. Créer un utilisateur : `POST /api/auth/register`
2. Se connecter : `POST /api/auth/login`
3. Cliquer sur `Authorize` dans Swagger et coller le token Bearer.

## Routes principales

Fournisseurs :

- `POST /api/fournisseurs`
- `GET /api/fournisseurs`
- `GET /api/fournisseurs/{id}`
- `PUT /api/fournisseurs/{id}`
- `DELETE /api/fournisseurs/{id}`

Produits :

- `POST /api/produits` avec `multipart/form-data`
- `GET /api/produits`
- `GET /api/produits/{id}`
- `PUT /api/produits/{id}`
- `DELETE /api/produits/{id}`
- `PATCH /api/produits/{id}/increment`
- `PATCH /api/produits/{id}/decrement`

Approvisionnements :

- `POST /api/approvisionnements`
- `GET /api/approvisionnements`
- `GET /api/approvisionnements/{id}`
- `PUT /api/approvisionnements/{id}`
- `DELETE /api/approvisionnements/{id}`

Lors de la création d'un approvisionnement, le stock du produit est augmenté automatiquement dans la même transaction.
