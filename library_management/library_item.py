from datetime import datetime
from uuid import uuid4



class LibraryItem:
    def __init__(
            self,
            title:str,
            pub_year:str,
            author_name:str,
            is_borrowed:bool = False,
            borrowed_by = None,
            due_date = None
    ):

        self.__item_id = str(uuid4())
        self.__title = title
        self.__author_name = author_name
        self.__pub_year = pub_year #Publish year
        self.__is_borrowed = is_borrowed
        self.__borrowed_by = borrowed_by
        self.__due_date = due_date


    def get_info(self) -> dict:
        """Get the attributes / details of the item"""
        borrowed_by = self.__borrowed_by if self.__borrowed_by is None else self.__borrowed_by.get_info()
        info = {
            "id": self.__item_id,
            "title": self.__title,
            "author_name": self.__author_name,
            "pub_year": self.__pub_year,
            "is_borrowed": self.__is_borrowed,
            "borrowed_by":borrowed_by,
            "due_date":self.__due_date
        }

        return info

    def get_id(self) -> str:
        return self.__item_id

    def get_due_date(self) -> datetime:
        return self.__due_date

    def get_title(self) -> str:
        return self.__title

    def get_author(self) -> str:
        return self.__author_name

    def get_borrowed_by(self):
        return self.__borrowed_by

    def get_is_borrowed(self) -> bool:
        return self.__is_borrowed

    def set_is_borrowed(self, value) -> None:
        self.__is_borrowed = value

    def set_due_date(self, value) -> None:
        self.__due_date = value

    def set_borrowed_by(self, value) -> None:
        self.__borrowed_by = value

    def is_overdue(self) -> bool:
        if not self.get_is_borrowed():
            raise Exception("Item not borrowed")

        return datetime.now() > self.__due_date

    def calculate_fine(self) -> int:
        if not self.get_is_borrowed():
            raise Exception("Cannot calculate fine: item has not been borrowed.")

        DAILY_FINE = 15
        MONTHLY_FINE = 500
        YEARLY_FINE = 10_000

        current_date = datetime.now()
        days_overdue = (current_date - self.__due_date).days

        if days_overdue < 1:
            return 0

        elif days_overdue < 30:
            return DAILY_FINE * days_overdue

        elif days_overdue < 365:
            months_overdue = days_overdue // 30
            return MONTHLY_FINE * months_overdue

        else:
            return YEARLY_FINE


class Book(LibraryItem):
    def __init__(
            self,
            title:str,
            pub_year:str,
            author_name:str,
            ISBN:str,
            is_borrowed=False,
            borrowed_by=None,
            due_date=None,

    ):
        super().__init__(
            title,
            pub_year,
            author_name,
            is_borrowed,
            borrowed_by,
            due_date
        )
        self.__ISBN = ISBN

    def get_info(self) -> dict:
        """Extend the parent get_info() with ISBN."""

        info = super().get_info()
        info["ISBN"] = self.__ISBN
        return info

class Magazine(LibraryItem):
    def __init__(
            self,
            title:str,
            pub_year:str,
            author_name:str,
            issue_no:str,
            is_borrowed=False,
            borrowed_by=None,
            due_date=None
    ):
        super().__init__(
            title,
            pub_year,
            author_name,
            is_borrowed,
            borrowed_by,
            due_date,
        )
        self.__issue_no = issue_no

    def get_info(self) -> dict:
        """Extend the parent get_info() with issue_no."""

        info = super().get_info()
        info["issue_no"] = self.__issue_no
        return info

class DVD(LibraryItem):
    def __init__(
            self,
            title:str,
            pub_year:str,
            author_name:str,
            duration:str,
            is_borrowed=False,
            borrowed_by=None,
            due_date=None
    ):
        super().__init__(
            title,
            pub_year,
            author_name,
            is_borrowed,
            borrowed_by,
            due_date
        )
        self.__duration = duration

    def get_info(self) -> dict:
        """Extend the parent get_info() with duration."""

        info = super().get_info()
        info["duration"] = self.__duration
        return info