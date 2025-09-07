# Exception map + quick handle for internal codes
```
           ┌───────────────────────┐
           │        User           │
           │  (Client / Frontend) │
           └──────────▲────────────┘
                      │
                      │ interacts
                      │
           ┌──────────┴────────────┐
           │       Auth Layer       │
           │-----------------------│
           │ Raises:               │
           │ - AuthError           │
           │   - AuthenticationError │
           │   - AuthorizationError  │
           │ Responsible for user  │
           │ identity verification │
           └──────────▲────────────┘
                      │
                      │ calls / forwards
                      │
           ┌──────────┴────────────┐
           │        API Layer       │
           │   (FastAPI Endpoints) │
           │-----------------------│
           │ Raises: ApiError      │
           │ Only exceptions visible│
           │ to clients            │
           └──────────▲────────────┘
                      │
                      │ orchestrates
                      │
           ┌──────────┴────────────┐
           │   Service / Domain     │
           │ (Business Logic Layer) │
           │-----------------------│
           │ Catches & wraps        │
           │ exceptions from DB    │
           │ and Cloud              │
           │ - DbError              │
           │ - CloudError           │
           │ - CoreError            │
           └───────▲───────▲───────┘
                   │       │
                   │       │
     ┌─────────────┘       └──────────────┐
     │                                    │
┌──────────────┐                    ┌──────────────┐
│   DB Layer    │                    │  Cloud Layer │
│--------------│                    │--------------│
│ Raises:      │                    │ Raises:      │
│ - DbError    │                    │ - CloudError │
│   - SqlError │                    │   - AWSError │
│   - MongoError│                   │   - AzureError│
│   - FsError  │                    │   - GCPError │
└──────────────┘                    └──────────────┘

Notes:
- Exceptions flow upward from DB/Cloud → Service → API → User.
- Auth layer is checked before API endpoints.
- Only API layer exposes exceptions to the user.
- Service layer may wrap, retry, or transform exceptions into API-friendly errors.
- DB & Cloud layers are unaware of API or Auth layers.
```
