from datetime import datetime
from uuid import uuid4



class LibraryItem:
    """
    Represents an item available in the library's collection.

    Attributes:
        __item_id (str): Unique identifier for the library item.
        __title (str): Title of the library item.
        __author_name (str): Name of the author who created the item.
        __pub_year (str): Year the item was published.
        __is_borrowed (bool): Indicates whether the item is currently borrowed.
        __borrowed_by (Member): The member in possession of the item.
        __due_date (datetime): The due date for returning the borrowed item.
    """


    def __init__(
            self,
            title:str,
            pub_year:str,
            author_name:str,
            is_borrowed:bool = False,
            borrowed_by = None,
            due_date = None
    ):
        """
        Initialize a new LibraryItem instance.

        :param title: Title of the item.
        :param pub_year: Year the item was published.
        :param author_name: Name of the item's author.
        :param is_borrowed: Whether the item is currently borrowed.
        :param borrowed_by: The Member object who borrowed the item, if any.
        :param due_date: The due date for the borrowed item, if applicable.
        """

        self.__item_id = str(uuid4())
        self.__title = title
        self.__author_name = author_name
        self.__pub_year = pub_year #Publish year
        self.__is_borrowed = is_borrowed
        self.__borrowed_by = borrowed_by
        self.__due_date = due_date


    def get_info(self) -> dict:
        """
        Retrieve detailed information about the library item.

        :return: A dictionary containing the item's details such as ID, title, author,
                 publication year, borrowed status, borrower info, and due date.
        """

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
        """Return the unique ID of the item."""
        return self.__item_id

    def get_due_date(self) -> datetime:
        """Return the due date of the item."""
        return self.__due_date

    def get_title(self) -> str:
        """Return the title of the item."""
        return self.__title

    def get_author(self) -> str:
        """Return the author name of the item."""
        return self.__author_name

    def get_borrowed_by(self):
        """Return member in possession of the item."""
        return self.__borrowed_by

    def get_is_borrowed(self) -> bool:
        """Return if item is borrowed, or not."""
        return self.__is_borrowed

    def set_is_borrowed(self, value) -> None:
        """
        Update the borrowed status of the item.

        :param value: True if the item is borrowed, False otherwise.
        """
        self.__is_borrowed = value

    def set_due_date(self, value) -> None:
        """
        Update the due_date of the item.

        :param value: A datetime object representing the new due date.
        """
        self.__due_date = value

    def set_borrowed_by(self, value) -> None:
        """
        Update the member who borrowed the item.

        :param value: The Member object who borrowed the item, or None if returned.
        """
        self.__borrowed_by = value

    def is_overdue(self) -> bool:
        """
        Check whether the item is overdue.

        :return: True if item is overdue, False otherwise.
        :raises Exception: If the item has not been borrowed.
        """
        if not self.get_is_borrowed():
            raise Exception("Item not borrowed")

        return datetime.now() > self.__due_date

    def calculate_fine(self) -> float:
        """
        Calculate the fine of the overdue item.

        :return: The fine amount in float currency units.
        :raises Exception: If the item has not been borrowed.
        """
        if not self.get_is_borrowed():
            raise Exception("Cannot calculate fine: item has not been borrowed.")

        DAILY_FINE = 15
        MONTHLY_FINE = 500
        YEARLY_FINE = 10_000

        current_date = datetime.now()
        days_overdue = (current_date - self.__due_date).days

        if days_overdue < 1:
            return float(0)

        elif days_overdue < 30:
            return float(DAILY_FINE * days_overdue)

        elif days_overdue < 365:
            months_overdue = days_overdue // 30
            return float(MONTHLY_FINE * months_overdue)

        else:
            return float(YEARLY_FINE)


class Book(LibraryItem):
    """
    Represents a book in the library.

    Attributes:
        __ISBN (str): The International Standard Book Number of the book.
    """
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
        """
        Initialize a new Book instance.

        :param title: Title of the book.
        :param pub_year: Year the book was published.
        :param author_name: Name of the book's author.
        :param ISBN: The International Standard Book Number.
        :param is_borrowed: Whether the book is currently borrowed.
        :param borrowed_by: The Member object who borrowed the book.
        :param due_date: The due date for the borrowed book.
        """
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
        """
        Extend the parent get_info() with ISBN.

        :return: A dictionary containing the book's details.
        """

        info = super().get_info()
        info["ISBN"] = self.__ISBN
        return info

class Magazine(LibraryItem):
    """
    Represents a magazine in the library.

    Attributes:
        __issue_no (str): The issue number of the magazine.
    """
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
        """
        Initialize a new Magazine instance.

        :param title: Title of the magazine.
        :param pub_year: Year the magazine was published.
        :param author_name: Name of the magazine's author or editor.
        :param issue_no: The issue number of the magazine.
        :param is_borrowed: Whether the magazine is currently borrowed.
        :param borrowed_by: The Member object who borrowed the magazine.
        :param due_date: The due date for the borrowed magazine.
        """

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
        """
        Extend the parent get_info() with issue_no.

        :return: A dictionary containing the magazine's details.
        """

        info = super().get_info()
        info["issue_no"] = self.__issue_no
        return info

class DVD(LibraryItem):
    """
    Represents a DVD in the library.

    Attributes:
        __duration (str): The duration of the DVD content.
    """
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
        """
        Initialize a new DVD instance.

        :param title: Title of the DVD.
        :param pub_year: Year the DVD was released.
        :param author_name: Name of the DVD's creator or director.
        :param duration: Duration of the DVD content.
        :param is_borrowed: Whether the DVD is currently borrowed.
        :param borrowed_by: The Member object who borrowed the DVD.
        :param due_date: The due date for the borrowed DVD.
        """
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
        """
        Extend the parent get_info() with duration.

        :return: A dictionary containing the DVD's details.
        """

        info = super().get_info()
        info["duration"] = self.__duration
        return info