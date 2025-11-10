from datetime import datetime, timedelta
from uuid import uuid4
from .library_item import LibraryItem


class Member:
    """
    Represents a library member who can borrow library items.

    Attributes:
        __member_id (str): Unique identifier for the member.
        __name (str): Name of the member.
        __borrowed_items (dict): Maps borrowed item IDs to LibraryItem objects.
    """

    def __init__(self, name:str):
        """
        Initialize a new Member instance.

        :param name: The name of the member.
        """
        self.__member_id = str(uuid4())
        self.__name = name
        self.__borrowed_items = {}

    def get_borrowed_items(self) -> list[dict]:
        """
        Retrieve information about all the items borrowed by the member.

        :return: A list of dictionaries representing the borrowed items.
        """

        return [item.get_info() for item in self.__borrowed_items.values()]

    def get_id(self) -> str:
        """
        Retrieve the unique ID of the member.

        :return: The member's ID as a string.
        """

        return self.__member_id

    def get_info(self) -> dict:
        """
        Retrieve basic information about the member.

        :return: Dictionary containing 'id' and 'name' keys.
        """

        return {
            "id": self.__member_id,
            "name":self.__name
        }

    def __calculate_due_date(self) -> datetime:
        """
        Calculate the due date of the borrowed item, which is four days from the current date.

        :return: A datetime object representing the due date.
        """
        return datetime.now() + timedelta(days=4)

    def borrow_item(self, item:LibraryItem) -> None:
        """
        Borrow library item and add it to the member's borrowed items.

        :param item: The LibraryItem object to borrow.
        :raises Exception: If the item has already been borrowed by the member.
        """
        if item.get_id() in self.__borrowed_items:
            raise Exception("Item already borrowed by you.")

        item.set_is_borrowed(True)
        item.set_borrowed_by(self)
        item.set_due_date(self.__calculate_due_date())

        self.__borrowed_items[item.get_id()] = item

    def return_item(self, item:LibraryItem) -> None:
        """
        Return a borrowed library item.

        :param item: The LibraryItem object to return.
        :raises Exception: If the member has not borrowed this item.
        """
        if item.get_id() not in self.__borrowed_items:
            raise Exception("Your have not borrowed this item.")

        item.set_is_borrowed(False)
        item.set_borrowed_by(None)
        item.set_due_date(None)

        del self.__borrowed_items[item.get_id()]