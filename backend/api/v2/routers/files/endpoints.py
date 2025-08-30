import fastapi
from fastapi.responses import StreamingResponse
from loguru import logger
import typing
import io, zipfile

# from . import response_examples
from backend.database import DatabaseInterface
from backend.database.file_storage import Record

files_router = fastapi.APIRouter(prefix="/files", tags=["Files"])

if typing.TYPE_CHECKING:
    from backend.database import FileStorageImplementation
FILE_NAME = str
CONTENT = bytes


@files_router.get("/file-names")
async def get_file_names(
    file_storage: typing.Annotated[
        "FileStorageImplementation",
        fastapi.Depends(DatabaseInterface.get_db_impl(db_name="FileStorage")),
    ],
    start: int = fastapi.Query(
        default=0,
        ge=0,
        le=999_999,
        description="Pagination start index",
    ),
    size: int = fastapi.Query(
        default=100,
        ge=1,
        le=100,
        description="Number of records to return per page",
    ),
) -> list[FILE_NAME]:
    return await file_storage.list_records(start=start, size=size)


@files_router.get("/", status_code=fastapi.status.HTTP_200_OK)
async def get_files(
    file_storage: typing.Annotated[
        "FileStorageImplementation",
        fastapi.Depends(DatabaseInterface.get_db_impl(db_name="FileStorage")),
    ],
    filenames: str | None = fastapi.Query(
        default=None,
        description="Comma-separated list of filenames to fetch",
        example="sample_0.pdf,sample_1.pdf",
    ),
    start: int = fastapi.Query(
        default=0,
        ge=0,
        le=100,
        description="Pagination start index",
    ),
    size: int = fastapi.Query(
        default=100,
        ge=1,
        le=100,
        description="Number of records to return per page",
    ),
) -> StreamingResponse:
    """Get files. Returns a downloadable ZIP with files.

    Retrieves records from file storage.
    If `filenames` is provided, only those are fetched.
    Otherwise, returns paginated list of records.

    <!--
    Internal developer notes, not visible in Swagger.
    Args:
        file_storage: (int) Session object for file storage.
        filenames: (str | None): Filenames to fetch.
        start: (int) Pagination start index.
        size: (int) Pagination size.

    Returns:
        StreamingResponse: Stream of ZIP with files.
    """
    if filenames:
        files: list[FILE_NAME] = [f.strip() for f in filenames.split(",")]
        records = await file_storage.get_many_records(files)
    else:
        records = await file_storage.list_records(start=start, size=size)

    logger.debug("Zipping files...")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for filename, content in records.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)
    logger.debug("Streaming files...")
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=files.zip"},
    )


# # ADD many files (multipart/form-data)
@files_router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def add_many_files(
    files: list[fastapi.UploadFile] = fastapi.File(...),
    file_storage: "FileStorageImplementation" = fastapi.Depends(
        DatabaseInterface.get_db_impl(db_name="FileStorage")
    ),
) -> dict[FILE_NAME, bool]:
    data = [Record(filename=f.filename, content=f.file.read()) for f in files]
    return await file_storage.add_many_records(records=data)


# DELETE many files by filename list
@files_router.delete("/")
async def delete_many_files(
    file_storage: typing.Annotated[
        "FileStorageImplementation",
        fastapi.Depends(DatabaseInterface.get_db_impl(db_name="FileStorage")),
    ],
    filenames: str = fastapi.Query(
        description="Comma-separated list of filenames to fetch",
        example="sample_0.pdf,sample_1.pdf",
    ),
) -> dict[FILE_NAME, bool]:
    files: list[FILE_NAME] = [f.strip() for f in filenames.split(",")]
    return await file_storage.delete_many_records(files)


@files_router.delete("/json")
async def delete_many_files(
    file_storage: typing.Annotated[
        "FileStorageImplementation",
        fastapi.Depends(DatabaseInterface.get_db_impl(db_name="FileStorage")),
    ],
    filenames: list[FILE_NAME] = fastapi.Body(
        ...,
        description="JSON list of filenames to delete",
        min_length=1,
        max_length=10,
        example=["sample_0.pdf", "sample_1.pdf"],
    ),
) -> dict[FILE_NAME, bool]:
    return await file_storage.delete_many_records(filenames)


# # UPDATE many files (multipart/form-data)
# @files_router.put("/many/update")
# async def update_many_files(
#     files: List[UploadFile] = File(...),ļ
#     append: bool = True,
#     file_storage: "FileStorageImplementation" = Depends(
#         DatabaseInterface.get_db_impl(db_name="FileStorage")
#     ),
# ) -> ORJSONResponse:
#     records = []
#     for f in files:
#         content = (await f.read()).decode("utf-8")
#         records.append(Record(filename=f.filename, content=content))
#     result = await file_storage.update_many_records(records, append=append)
#     return ORJSONResponse(result)
#
#
