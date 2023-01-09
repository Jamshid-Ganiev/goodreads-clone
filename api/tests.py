from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='james', first_name='Jamshid')
        self.user.set_password('password11')
        self.user.save()
        self.client.login(username='james', password='password11')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Nice book")

        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], "Book1")
        self.assertEqual(response.data['book']['description'], "Description1")
        self.assertEqual(response.data['book']['isbn'], "1111")

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], 'james')
        self.assertEqual(response.data['user']['first_name'], 'Jamshid')

    def test_delete_review(self):
        book = Book.objects.create(title='Sports', description='Healthy body', isbn='7777')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Useful book")

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='Sports', description='Healthy body', isbn='7777')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Useful book")

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), data={'stars_given': 2})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 2)

    def test_put_review(self):
        """UPDATE REVIEW"""
        book = Book.objects.create(title='Big Money', description='are we rich?', isbn='1111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=3, comment="Useful book")

        response = self.client.put(
            reverse('api:review-detail', kwargs={'id': br.id}),
            data={'stars_given': 5, 'comment': "worth-reading book", 'user_id': self.user.id, 'book_id': book.id}
        )
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)
        self.assertEqual(br.comment, 'worth-reading book')

    def test_create_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111')
        data = {
            'stars_given': 4,
            'comment': "Good Book",
            'user_id': self.user.id,
            'book_id': book.id
        }

        response = self.client.post(reverse('api:review-list'), data=data)

        self.assertEqual(response.status_code, 201)
        br = BookReview.objects.get(book=book)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, "Good Book")

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='somebody', first_name='Someone')
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=1, comment="Awful book")

        response = self.client.get(reverse('api:review-list'))
        br.refresh_from_db()
        br_two.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], 1)
        self.assertEqual(response.data['results'][0]['comment'], "Awful book")
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][1]['comment'], "Nice book")
