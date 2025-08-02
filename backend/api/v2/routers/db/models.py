from enum import Enum

class AllowedDbMethod(str, Enum):
    get_record = "get_record"
    get_many_records = "get_many_records"
    add_record = "add_record"
    add_many_records = "add_many_records"
    update_record = "update_record"
    update_many_records = "update_many_records"
    delete_record = "delete_record"
    delete_many_records = "delete_many_records"
