from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


# Create your tests here.
class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        book1 = Book.objects.create(title='Book1', description='description1', isbn='1111')
        book2 = Book.objects.create(title='Book2', description='description2', isbn='2222')
        book3 = Book.objects.create(title='Book3', description='description3', isbn='3333')

        response = self.client.get(reverse('books:list') + "?page_size=2")
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1111')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='description1', isbn='1111')
        book2 = Book.objects.create(title='Guide', description='description2', isbn='2222')
        book3 = Book.objects.create(title='Business', description='description3', isbn='3333')

        response = self.client.get(reverse("books:list") + "?q=Sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Guide")
        self.assertNotContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Business")
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertContains(response, book3.title)


class BookReviewTest(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn="7777")
        user = CustomUser.objects.create(
            username='james', first_name='Jamshid', last_name='Ganiev', email='jganiev@gmail.com'
        )
        user.set_password('password33')
        user.save()
        self.client.login(username='james', password='password33')

        self.client.post(reverse('books:reviews', kwargs={'id': book.id}), data={
            'stars_given': 2,
            'comment': 'This book is nice to read.'
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 2)
        self.assertEqual(book_reviews[0].comment, 'This book is nice to read.')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)

