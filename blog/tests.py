from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

class BlogTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            body='This is a test post.',
            author=self.user
        )

    def test_str_representation(self):
        post = Post(title='Test Post', body='This is a test post.', author=self.user)
        self.assertEqual(str(post), 'Test Post')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Test Post')
        self.assertEqual(f'{self.post.body}', 'This is a test post.')
        self.assertEqual(f'{self.post.author}', 'testuser')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post.')
        self.assertTemplateUsed(response, 'home.html')
       
    def test_detail_view(self):
        # Test valid post detail view
        response = self.client.get(reverse('post_detal', args=[self.post.pk]))  # Fixed URL name and args
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'post_detal.html')  # Fixed template name
        
        # Test invalid post ID
        invalid_response = self.client.get(reverse('post_detal', args=[999]))  # Use reverse for invalid case
        self.assertEqual(invalid_response.status_code, 404)

    def test_create_post_view(self):
        self.client.login(username='testuser', password='secret')  # Log in the user
        response = self.client.post(reverse('new_post'), {
            'title': 'New Post',
            'body': 'New post content',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after creation
        self.assertTrue(Post.objects.filter(title='New Post').exists())  # Verify post is created
    def test_update_post_view(self):
        self.client.login(username='testuser', password='secret')  # Log in the user
        response = self.client.post(reverse('post_edit', args=[self.post.pk]), {
            'title': 'Updated Post',
            'body': 'Updated post content',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after update
        self.post.refresh_from_db()  # Refresh the post instance from the database
        self.assertEqual(self.post.title, 'Updated Post')  # Verify title is updated

    def test_delete_post_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful deletion
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())  # Check if post is deleted
