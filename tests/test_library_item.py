from datetime import datetime, timedelta
from library_management.library_item import LibraryItem, Book, DVD, Magazine

import unittest

from library_management.member import Member


class TestLibraryItem(unittest.TestCase):

    def setUp(self):

        self.member = Member(name="Patrick")

        self.library_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli"
        )

        self.not_overdue_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() + timedelta(days=4)  # four days after creation
        )

        self.two_days_due_borrowed_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() - timedelta(days=2)  # two days before creation
        )

        self.two_months_due_borrowed_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() - timedelta(days=60)  # Two month before creation
        )

        self.one_year_due_borrowed_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() - timedelta(days=365)  # A year before creation
        )

        self.two_years_due_borrowed_item = LibraryItem(
            title="The Art of Thinking Clearly",
            pub_year="2013",
            author_name="Rolf Dobelli",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() - timedelta(days=750)  # two years before creation
        )

    def test_self_isinstance_library_item(self):
        self.assertIsInstance(self.library_item, LibraryItem)

    def test_library_item_creation(self):
        info = self.library_item.get_info()

        self.assertNotEqual(info.get("id"), "")
        self.assertEqual(info.get("title"), "The Art of Thinking Clearly")
        self.assertEqual(info.get("pub_year"), "2013")
        self.assertEqual(info.get("author_name"), "Rolf Dobelli")
        self.assertEqual(info.get("is_borrowed"), False)
        self.assertEqual(info.get("borrowed_by"), None)
        self.assertEqual(info.get("due_date"), None)

        with self.assertRaises(Exception):
            self.library_item.is_overdue()
            self.library_item.calculate_fine()


    def test_can_not_access_private_attributes(self):
        with self.assertRaises(AttributeError):
            self.library_item.__title
            self.library_item.__item_id
            self.library_item.__pub_year
            self.library_item.__author_name
            self.library_item.__is_borrowed
            self.library_item.__borrowed_by
            self.library_item.__due_date

    def test_calculate_fine(self):
        two_days_overdue = self.two_days_due_borrowed_item.calculate_fine()
        two_months_overdue = self.two_months_due_borrowed_item.calculate_fine()
        one_year_overdue = self.one_year_due_borrowed_item.calculate_fine()
        two_years_overdue = self.two_years_due_borrowed_item.calculate_fine()
        not_overdue = self.not_overdue_item.calculate_fine()

        self.assertEqual(not_overdue, 0.00)
        self.assertEqual(two_days_overdue, 30.00)
        self.assertEqual(two_months_overdue, 1_000.00)
        self.assertEqual(one_year_overdue, 10_000.00)
        self.assertEqual(two_years_overdue, 10_000.00)


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book(
            title="The Pragmatic Programmer",
            pub_year="1999",
            author_name="Andrew Hunt and David Thomas",
            ISBN="978-0201616224"
        )

    def test_self_isinstance_of_Book_and_LibraryItem(self):
        self.assertIsInstance(self.book, Book)
        self.assertIsInstance(self.book, LibraryItem)

    def test_Book_is_subclass_of_LibraryItem(self):
        self.assertTrue(issubclass(Book, LibraryItem))

    def test_book_extended_get_info(self):
        info = self.book.get_info()
        ISBN = info.get("ISBN")

        self.assertIn("ISBN", info)
        self.assertEqual(ISBN, "978-0201616224")

class TestMagazine(unittest.TestCase):
    def setUp(self):
        self.magazine = Magazine(
            title="National Geographic",
            pub_year="2023",
            author_name="Susan Goldberg",
            issue_no="May 2023 Issue"
        )

    def test_self_isinstance_of_Magazine_and_LibraryItem(self):
        self.assertIsInstance(self.magazine, Magazine)
        self.assertIsInstance(self.magazine, LibraryItem)

    def test_Magazine_is_subclass_of_LibraryItem(self):
        self.assertTrue(issubclass(Magazine, LibraryItem))

    def test_magazine_extended_get_info(self):
        info = self.magazine.get_info()
        issue_no = info.get("issue_no")

        self.assertIn("issue_no", info)
        self.assertEqual(issue_no, "May 2023 Issue")


class TestDVD(unittest.TestCase):
    def setUp(self):
        self.dvd = DVD(
            title="Inception",
            pub_year="2010",
            author_name="Christopher Nolan",
            duration="2h:28m"
        )

    def test_self_isinstance_of_DVD_and_LibraryItem(self):
        self.assertIsInstance(self.dvd, DVD)
        self.assertIsInstance(self.dvd, LibraryItem)

    def test_DVD_is_subclass_of_LibraryItem(self):
        self.assertTrue(issubclass(DVD, LibraryItem))

    def test_DVD_extended_get_info(self):
        info = self.dvd.get_info()
        duration = info.get("duration")

        self.assertIn("duration", info)
        self.assertEqual(duration, "2h:28m")
