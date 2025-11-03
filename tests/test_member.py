from library_management.member import Member
from library_management.library_item import Book
import unittest

class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member(name="Patrick")

        self.book = Book(
            title="The Pragmatic Programmer",
            pub_year="1999",
            author_name="Andrew Hunt and David Thomas",
            ISBN="978-0201616224"
        )


    def test_member_creation(self):
        info = self.member.get_info()

        self.assertEqual(info.get("name"), "Patrick")
        self.assertNotEqual(info.get("id"), "")
        self.assertEqual(self.member.get_borrowed_items(), [])

    def test_can_not_access_private_attributes(self):
        with self.assertRaises(AttributeError):
            self.member.__name
            self.member.__member_id
            self.member.__borrowed_items

    def test_borrow_item(self):
        self.member.borrow_item(item=self.book)
        borrowed_items = self.member.get_borrowed_items()
        borrowed_by = self.book.get_borrowed_by()
        borrowed_by_id = borrowed_by.get_id()

        self.assertEqual(len(borrowed_items), 1)
        self.assertEqual(self.member.get_id(), borrowed_by_id)
        self.assertIsNotNone(self.book.get_due_date())
        self.assertTrue(self.book.get_is_borrowed())

    def test_return_item(self):
        self.member.borrow_item(item=self.book)
        self.member.return_item(item=self.book)
        borrowed_items = self.member.get_borrowed_items()

        self.assertEqual(len(borrowed_items), 0)
        self.assertIsNone(self.book.get_borrowed_by())
        self.assertIsNone(self.book.get_due_date())
        self.assertFalse(self.book.get_is_borrowed())