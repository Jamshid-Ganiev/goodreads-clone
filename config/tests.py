from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1', description='description1', isbn="007700")
        user = CustomUser.objects.create(
            username='james', first_name='Jamshid', last_name='Ganiev', email='james@gmail.com'
        )
        user.set_password("qwerty")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Best Book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Useful Book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=2, comment="Good Book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
