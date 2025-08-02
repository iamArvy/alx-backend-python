from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessagingTests(TestCase):
    def setUp(self):
        """Create test data that ALL tests will use"""
        self.sender = User.objects.create_user(
            username='sender', 
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', 
            password='testpass123'
        )
        
        # Sample message for tests that need it
        self.test_message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Initial test message"
        )

    def tearDown(self):
        """Clean up after each test"""
        # Clear all created objects
        User.objects.all().delete()
        Message.objects.all().delete()
        Notification.objects.all().delete()

    def test_message_creation(self):
        """Verify message creation works"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="New test message"
        )
        self.assertEqual(message.sender.username, 'sender')
        
    def test_notification_auto_creation(self):
        """Verify signals create notifications"""
        initial_count = Notification.objects.count()
        
        new_message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Trigger notification"
        )
        
        self.assertEqual(
            Notification.objects.count(),
            initial_count + 1
        )
        notification = Notification.objects.first()
        self.assertIsNotNone(notification, "No Notification object found")
        if notification:
            self.assertEqual(
                notification.message,
                new_message
            )
            self.assertEqual(
                notification.user,
                self.receiver
            )