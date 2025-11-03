from .library_item import LibraryItem
from .member import Member


class Library:
    def __init__(self):
        self.__items = {}
        self.__members = {}

    def add_item(self, item:LibraryItem) -> None:
        if not isinstance(item, LibraryItem):
            raise ValueError("item must be a valid LibraryItem object.")

        self.__items[item.get_id()]=item

    def remove_item(self, item_id:str) -> None:
        item = self.__items.get(item_id)
        if item is None:
            raise KeyError(f"item with the {item_id} doe not exist.")

        del self.__items[item_id]

    def search_item(
            self,
            title:str = None,
            author_name:str = None,
            item_id:str = None
    ) -> list[LibraryItem]:

        if title is author_name is item_id is None:
            raise Exception("Item title, author_name and item_id can not be empty.")

        def matches(item):
            if title and item.get_title() != title:
                return False
            if author_name and item.get_author() != author_name:
                return False
            if item_id and item.get_id() != item_id:
                return False
            return True

        return [item for item in self.__items.values() if matches(item)]

    def get_items(self) -> list[dict]:
        return [item.get_info() for item in self.__items.values()]

    def create_member(self, name:str) -> str:
        if not isinstance(name, str):
            raise ValueError(f"{name} have to be of type string.")

        member = Member(name=name)
        self.__members[member.get_id()]=member

        return member.get_id()

    def get_members(self) -> list[dict]:
        return [member.get_info() for member in self.__members.values()]


    def lend_item(self, member_id:str, item:LibraryItem) -> None:
        if member_id not in self.__members:
            raise Exception("Member with that id does not exist.")

        if item.get_id() not in self.__items:
            raise Exception("Item does not exist in library.")

        member = self.__members.get(member_id)
        member.borrow_item(item)

    def return_item(self, member_id:str, item:LibraryItem) -> None:
        if member_id not in self.__members:
            raise Exception("Member with that id does not exist.")

        if item.get_id() not in self.__items:
            raise Exception("Item does not exist in library.")

        member = self.__members.get(member_id)
        member.return_item(item)

    def get_overdue_items(self) -> list[LibraryItem]:
        items = self.__items.values()

        return [item for item in items if item.is_overdue()]
