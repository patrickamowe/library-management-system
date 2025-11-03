from datetime import datetime, timedelta
from uuid import uuid4
from .library_item import LibraryItem


class Member:
    def __init__(self, name:str):
        self.__member_id = str(uuid4())
        self.__name = name
        self.__borrowed_items = {}

    def get_borrowed_items(self) -> list[dict]:
        """Get borrowed items"""

        return [item.get_info() for item in self.__borrowed_items.values()]

    def get_id(self) -> str:
        """Get member id"""

        return self.__member_id

    def get_info(self) -> dict:

        return {
            "id": self.__member_id,
            "name":self.__name
        }

    def __calculate_due_date(self) -> datetime:
        return datetime.now() + timedelta(days=4)

    def borrow_item(self, item:LibraryItem) -> None:
        if item.get_id() in self.__borrowed_items:
            raise Exception("Item already borrowed by you.")

        item.set_is_borrowed(True)
        item.set_borrowed_by(self)
        item.set_due_date(self.__calculate_due_date())

        self.__borrowed_items[item.get_id()] = item

    def return_item(self, item:LibraryItem) -> None:
        if item.get_id() not in self.__borrowed_items:
            raise Exception("Your have not borrowed this item.")

        item.set_is_borrowed(False)
        item.set_borrowed_by(None)
        item.set_due_date(None)

        del self.__borrowed_items[item.get_id()]