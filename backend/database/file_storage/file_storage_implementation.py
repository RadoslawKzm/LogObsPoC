import pathlib
from enum import StrEnum

from loguru import logger

from backend.api.v2.exceptions import db_exceptions
from backend.database.interface import DatabaseInterface
from backend.database.file_storage import FileStorageSessionManager
from backend.database.models import FlowControl
from .models import Record

CURRENT_FILE = pathlib.Path(__file__).parent
DATA_FOLDER = CURRENT_FILE / "data"
DATA_FOLDER.mkdir(exist_ok=True)
FILENAME = str
CONTENT = str


def _get_file_path(
    *,
    filename: str,
    flow_control: FlowControl = FlowControl.BOOL,
) -> pathlib.Path | bool:
    """Get the full path of a file in the data folder.

    Args:
        filename (str): The name of the file.
        flow_control (FlowControl, optional): Raise exception or return False.
    Returns:
        pathlib.Path | bool: Path to the file, or False if file not found &&
                                            flow_control == FlowControl.BOOL
    Raises:
        db_exceptions.file_storage.FileNotFound: If the file does not exist &&
                                        flow_control == FlowControl.EXCEPTIONS
    """
    path = DATA_FOLDER / filename
    if not path.exists():
        if flow_control == FlowControl.BOOL:
            return False
        msg: str = f"No filename: {filename} found"
        raise db_exceptions.file_storage.FileNotFound(
            internal_message=msg,
            external_message=msg,
        )
    return path


class FileStorageImplementation(DatabaseInterface):
    database_name = "FileStorage"
    session_factory = FileStorageSessionManager()

    def __init__(self, *args, session, **kwargs) -> None:
        self.session = session

    async def get_record(
        self,
        record: Record,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> Record:
        """Read the content of a file.

        Args:
            record (Record): The record to get. Has fields:
                filename (str): Name of the file to read.
                content (str): Content, for GET operations None.
            flow_control (FlowControl, optional): Raise exc or return False
        Returns:
            Record: Filename and file contents.
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.opt(lazy=True).debug(
            "Getting file: {f_name} from File Storage",
            f_name=lambda: record.filename,
        )
        path: pathlib.Path | None = _get_file_path(
            filename=str(record.filename),
            flow_control=flow_control,
        )
        if not path:
            logger.opt(lazy=True).debug(
                "Cannot get file:{f_name}",
                f_name=lambda: record.filename,
            )
            return Record(filename=record.filename, content=False)
        return Record(
            filename=record.filename,
            content=path.read_text(encoding="utf-8"),
        )

    async def get_many_records(
        self,
        records: list[Record],
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> dict[FILENAME, CONTENT]:
        """Reads the contents of a multiple files.

        Args:
            records (list[Record]): List of file contents to read. Has fields:
                filename (str): Name of the file to create.
                content (str): Content, for GET operations None.
            flow_control (FlowControl, optional): Raise exc or return False
        Returns:
            Mapping of filenames to their contents.
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.debug("Getting multiple records from File Storage")
        results = {}
        for record in records:
            result: Record = await self.get_record(
                record=record,
                flow_control=flow_control,
            )
            results[result.filename] = result.content
        return results

    async def list_records(
        self,
        start: int = 0,
        size: int = 100,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> dict[FILENAME, CONTENT]:
        """Returns all files in the data folder.

        Returns:
            dict[FILENAME, Record]: Dict of filenames with contents
                                            present in data folder.
        """
        logger.opt(lazy=True).debug(
            "Getting records. "
            "Starting at index:{start} with size:{size} from File Storage...",
            start=lambda: start,
            size=lambda: size,
        )
        files: dict[FILENAME, CONTENT] = {}
        for file in DATA_FOLDER.iterdir():
            if not file.is_file():
                continue
            result: Record = await self.get_record(
                record=Record(filename=file.name),
                flow_control=flow_control,
            )
            files[result.filename] = result.content
        return {
            k: v for k, v in list(sorted(files.items()))[start : start + size]
        }

    async def add_record(
        self,
        record: Record,
        overwrite: bool = False,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> Record:
        """Create a new file with the given content. Overwrites OFF by default.

        Args:
            record (Record): The record to add. Has fields:
                filename (str): Name of the file to create.
                content (str): Text content to write into the file.
            overwrite (bool, optional): Overwrite existing file. Defaults False
            flow_control (FlowControl, optional): Raise exc or return False
        Returns:
            Record: filename and content as boolean state of creating. Content:
                True if records was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileAlreadyExists:
                                    If the file exist && overwrite is False &&
                                    flow_control == FlowControl.EXCEPTIONS
        """
        logger.opt(lazy=True).debug(
            "Adding file:{f_name} to File Storage",
            f_name=lambda: record.filename,
        )
        path = DATA_FOLDER / record.filename
        if path.exists() and not overwrite:
            logger.opt(lazy=True).debug(
                "Unable to create file:{f_name}, already exists in FS",
                f_name=lambda: record.filename,
            )
            if flow_control == FlowControl.EXCEPTIONS:
                raise db_exceptions.file_storage.FileAlreadyExists(
                    f"File '{record.filename}' exist and {overwrite=}"
                )
            logger.opt(lazy=True).debug(
                "Returning record=False due to flow_control:{flow_control}",
                flow_control=lambda: flow_control,
            )
            return Record(filename=record.filename, content=False)
        path.write_text(record.content, encoding="utf-8")
        logger.opt(lazy=True).debug(
            "Added file:{f_name} to File Storage",
            f_name=lambda: record.filename,
        )
        return Record(filename=record.filename, content=True)

    async def add_many_records(
        self,
        records: list[Record],
        overwrite: bool = False,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> dict[FILENAME, bool]:
        """Creates a new files with the given contents. Does not overwrite.
        Overwrite can be set to True.

        Args:
            records (list[Record]): List of records to add. Record has fields:
                filename (str): Name of the file to create.
                content (str): Text content to write into the file.
            overwrite (bool, optional): Overwrite existing file. Defaults False
            flow_control (FlowControl, optional): Raise exc or return False
        Returns:
            Dict of filename and content as boolean state of creating. Content:
                True if record was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileAlreadyExists:
                                    If the file exist && overwrite is False &&
                                    flow_control == FlowControl.EXCEPTIONS
        """
        logger.debug("Adding many files to File Storage")
        results: dict[FILENAME, bool] = {}
        for record in records:
            result: Record = await self.add_record(
                record=record,
                overwrite=overwrite,
                flow_control=flow_control,
            )
            results[record.filename] = result.content
        return results

    async def update_record(
        self,
        record: Record,
        append: bool = True,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> Record:
        """Update the content of an existing file.
        By default, appends content to the file.
        If append=False, the file is overwritten.

        Args:
            record (Record): The record to add. Has fields:
                filename (str): Name of the file to create.
                content (str): Text content to write into the file.
            append (bool, optional): If to append to the file. Defaults to True
            flow_control (FlowControl, optional): Raise exc or return False
        Returns:
            Record: filename and content as boolean state of update. Content:
                True if record was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.opt(lazy=True).debug(
            "Updating {f_name} in File Storage",
            f_name=lambda: record.filename,
        )
        path: pathlib.Path = _get_file_path(
            filename=record.filename,
            flow_control=flow_control,
        )
        # Don't need to check for flow_control.
        if not path:  # If true, code would raise above already :)
            logger.opt(lazy=True).debug(
                "Cannot update file:{f_name}",
                f_name=lambda: record.filename,
            )
            return Record(filename=record.filename, content=False)
        if not append:
            path.write_text(record.content, encoding="utf-8")
            return Record(filename=record.filename, content=True)
        with path.open(mode="a", encoding="utf-8") as file:
            file.write(record.content)
        return Record(filename=record.filename, content=True)

    async def update_many_records(
        self,
        records: list[Record],
        append: bool = True,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> dict[FILENAME, bool]:
        """Update the contents of an existing files.
        By default, appends contents to the files.
        If append=False, the file is overwritten.

        Args:
            records (dict[FILENAME, bool]): List of updated files.
            append (bool, optional): If to append to the file. Defaults to True
            flow_control (FlowControl, optional): Raises exc or returns BOOL
        Returns:
            Dict of filename and content as boolean state of update. Content:
                True if record was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.debug("Updating many files in File Storage")
        results: dict[FILENAME, bool] = {}
        for record in records:
            result: Record = await self.update_record(
                record=record,
                append=append,
                flow_control=flow_control,
            )
            results[result.filename] = result.content
        return results

    async def delete_record(
        self,
        record: Record,
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> Record:
        """Deletes a file.

        Args:
            record (Record): The record to delete. Has fields:
                filename (str): Name of the file to create.
                content (str): For delete can be None
            flow_control (FlowControl, optional): Raises exc or returns BOOL
        Returns:
            Record: filename and content as boolean state of delete. Content:
                True if record was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.opt(lazy=True).debug(
            "Deleting {f_name} from File Storage",
            f_name=lambda: record.filename,
        )
        path: pathlib.Path = _get_file_path(
            filename=record.filename,
            flow_control=flow_control,
        )
        # Don't need to check for flow_control.
        if not path:  # If true, code would raise above already :)
            logger.opt(lazy=True).debug(
                "Cannot delete file:{f_name}",
                f_name=lambda: record.filename,
            )
            return Record(filename=record.filename, content=False)
        path.unlink()
        return Record(filename=record.filename, content=True)

    async def delete_many_records(
        self,
        records: list[Record],
        flow_control: FlowControl = FlowControl.BOOL,
    ) -> dict[FILENAME, bool]:
        """Deletes multiple files.

        Args:
            records (list[Record]): List of records to delete. Has fields:
                filename (str): Name of the file to create.
                content (str): For delete can be None
            flow_control (FlowControl, optional): Raises exc or returns BOOL
        Returns:
            Dict of filename and content as boolean state of delete. Content:
                True if record was added,
                False if flow_control == FlowControl.BOOL
        Raises:
            db_exceptions.file_storage.FileNotFound: If file doesn't exist &&
                                        flow_control == FlowControl.EXCEPTIONS
        """
        logger.debug("Deleting many files in File Storage")
        results: dict[FILENAME, bool] = {}
        for record in records:
            result: Record = await self.delete_record(
                record=record,
                flow_control=flow_control,
            )
            results[result.filename] = result.content
        return results
