from .library_item import LibraryItem
from .member import Member


class Library:
    """
    Represents a library that manages collections of items and registered members.

    Attributes:
        __items (dict): Maps item IDs to LibraryItem objects.
        __members (dict): Maps member IDs to Member objects.
    """


    def __init__(self):
        """Initialize a new Library instance."""
        self.__items = {}
        self.__members = {}

    def add_item(self, item:LibraryItem) -> None:
        """
        Add a new LibraryItem to the library's collection.

        :param item: The LibraryItem object to add.
        :raises ValueError: If the provided item is not a valid LibraryItem instance.
        """
        if not isinstance(item, LibraryItem):
            raise ValueError("item must be a valid LibraryItem object.")

        self.__items[item.get_id()]=item

    def remove_item(self, item_id:str) -> None:
        """
        Remove a LibraryItem from the  collection.

        :param item_id: The unique identifier of the item to remove.
        :raises KeyError: If no item with the given ID exists in the library.
        """
        item = self.__items.get(item_id)
        if item is None:
            raise KeyError(f"item with the {item_id} does not exist.")

        del self.__items[item_id]

    def search_item(
            self,
            keyword:str
    ) -> list[LibraryItem]:
        """
        Search the library's collection for items matching a keyword in their
        ID, title, or author name.

        :param keyword: The search term to look for.
        :return: A list of LibraryItem objects matching the keyword.
        """

        return [item for item in filter(
               lambda item: keyword in [item.get_id(), item.get_title(), item.get_author()],
                self.__items.values()
            )]

    def get_items(self) -> list[dict]:
        """Return information about all items in the library."""
        return [item.get_info() for item in self.__items.values()]

    def create_member(self, name:str) -> str:
        """
        Create and register a new member in the library.

        :param name: The name of the new member.
        :return : The unique ID of the created member.
        :raises ValueError: If provided name is not a string.
        """
        if not isinstance(name, str):
            raise ValueError(f"{name} have to be of type string.")

        member = Member(name=name)
        self.__members[member.get_id()]=member

        return member.get_id()

    def get_members(self) -> list[dict]:
        """Return information about all registered library members."""
        return [member.get_info() for member in self.__members.values()]


    def lend_item(self, member_id:str, item:LibraryItem) -> None:
        """
        lend a library item to a registered member.

        :param member_id: The unique ID of the member borrowing the item.
        :param item: The LibraryItem object to lend.
        :raises Exception: If the member or item does not exist in the library.
        """
        if member_id not in self.__members:
            raise Exception("Member with that id does not exist.")

        if item.get_id() not in self.__items:
            raise Exception("Item does not exist in library.")

        member = self.__members.get(member_id)
        member.borrow_item(item)

    def return_item(self, member_id:str, item:LibraryItem) -> None:
        """
        Process the return of a borrowed library item.

        :param member_id: The unique ID of the member returning the item.
        :param item: The LibraryItem object to be returned.
        :raises Exception: If the member or item does not exist in the library.
        """
        if member_id not in self.__members:
            raise Exception("Member with that id does not exist.")

        if item.get_id() not in self.__items:
            raise Exception("Item does not exist in library.")

        member = self.__members.get(member_id)
        member.return_item(item)

    def get_overdue_items(self) -> list[LibraryItem]:
        """
        Retrieve all overdue library items.

        :return: A list of LibraryItem objects that are overdue.
        """
        items = self.__items.values()

        return [item for item in items if item.is_overdue()]
