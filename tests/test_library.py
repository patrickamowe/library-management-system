from datetime import datetime, timedelta

from library_management.library import Library
from library_management.library_item import Book, Magazine, DVD
from library_management.member import Member

import unittest

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()

        self.member = Member(name="Patrick")

        self.book = Book(
            title="The Pragmatic Programmer",
            pub_year="1999",
            author_name="Andrew Hunt and David Thomas",
            ISBN="978-0201616224"
        )

        self.magazine = Magazine(
            title="National Geographic",
            pub_year="2023",
            author_name="Susan Goldberg",
            issue_no="May 2023 Issue"
        )

        self.dvd = DVD(
            title="Inception",
            pub_year="2010",
            author_name="Christopher Nolan",
            duration="2h:28m"
        )

        self.two_days_due_borrowed_item = Book(
            title="The Pragmatic Programmer",
            pub_year="1999",
            author_name="Andrew Hunt and David Thomas",
            ISBN="978-0201616224",
            is_borrowed=True,
            borrowed_by=self.member,
            due_date=datetime.now() - timedelta(days=2)  # two days before creation
        )

    def test_self_isinstance_of_Library(self):
        self.assertTrue(isinstance(self.library, Library))

    def test_add_item_to_library(self):
        self.library.add_item(self.book)
        items = self.library.get_items()

        self.assertNotEqual(items, [])
        self.assertEqual(len(items), 1)

    def test_remove_item_from_library(self):
        item = self.book
        self.library.add_item(item)
        self.library.remove_item(item.get_id())
        
        self.assertEqual(self.library.get_items(), [])

        with self.assertRaises(KeyError):
            self.library.remove_item(item.get_id())

    def test_create_library_member(self):
        member_id = self.library.create_member("Patrick")
        members = self.library.get_members()

        self.assertNotEqual(members, [])
        self.assertEqual(len(members), 1)
        self.assertEqual(member_id, members[0].get("id"))

    def test_lend_item(self):
        self.library.add_item(self.book)
        member_id = self.library.create_member(name="Patrick")

        self.library.lend_item(member_id=member_id, item=self.book)
        borrowed_by = self.book.get_borrowed_by()
        borrowed_by_id = borrowed_by.get_id()

        self.assertEqual(member_id, borrowed_by_id)
        self.assertIsNotNone(self.book.get_due_date())
        self.assertTrue(self.book.get_is_borrowed())

    def test_return_item(self):
        self.library.add_item(self.book)
        member_id = self.library.create_member(name="Patrick")

        self.library.lend_item(member_id=member_id, item=self.book)
        self.library.return_item(member_id=member_id, item=self.book)

        self.assertIsNone(self.book.get_borrowed_by())
        self.assertIsNone(self.book.get_due_date())
        self.assertFalse(self.book.get_is_borrowed())

    def test_overdue_items(self):
        self.library.add_item(self.two_days_due_borrowed_item)

        overdue_items = self.library.get_overdue_items()
        item = overdue_items[0]

        self.assertEqual(len(overdue_items), 1)
        self.assertTrue(item.is_overdue())
        self.assertEqual(item.calculate_fine(), 30)

    def test_search_item(self):
        self.library.add_item(self.book)
        self.library.add_item(self.magazine)
        self.library.add_item(self.dvd)

        result1 = self.library.search_item(title="The Pragmatic Programmer")
        result2 = self.library.search_item(author_name="Susan Goldberg")
        result3 = self.library.search_item(item_id=self.dvd.get_id())

        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0].get_id(), self.book.get_id())
        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0].get_id(), self.magazine.get_id())
        self.assertEqual(len(result3), 1)
        self.assertEqual(result3[0].get_id(), self.dvd.get_id())

        with self.assertRaises(Exception):
            self.library.search_item()
        
