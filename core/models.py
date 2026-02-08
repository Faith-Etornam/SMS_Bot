from django.db import models

# Create your models here.
class SMSUser(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, db_index=True, help_text="Format +233")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    credits = models.IntegerField(default=10, help_text="Number of free queries remaining")
    is_active = models.BooleanField(default=True, help_text='If False, user receives no replies')

    class Meta:
        verbose_name = 'SMS User'
        verbose_name_plural = 'SMS Users'

    def __str__(self):
        return f"{self.phone_number} {self.credits} credits left"
    
class Conversation(models.Model):

    """
    Stores the history of messages. 
    Essential for context (remembering previous questions).
    """

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('flagged', 'Flagged by AI') 
    ]

    user = models.ForeignKey(SMSUser, on_delete=models.CASCADE)
    incoming_message = models.TextField(help_text="What the user sent")
    ai_reponse = models.TextField(help_text='What the AI replied')
    input_tokens = models.IntegerField(default=0, help_text="Cost of user query")
    output_tokens = models.IntegerField(default=0, help_text="Cost of AI response")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    error_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.created_at.strftime('%Y-%m-%d %H:%M')}" 

    class Meta:
        ordering = ['-created_at']


