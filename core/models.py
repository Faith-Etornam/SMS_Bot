from django.db import models

# Create your models here.
class SMSUser(models.Model):

    """
    Model for Users sending sms to the AI model
    """
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

class SystemConfig(models.Model):

    """
    Singleton model to control the bot settings dynamically from Django Admin.
    You never need to redeploy code to change the prompt.
    """

    active = models.BooleanField(default=True, help_text='If False, bot replies with Maintenance Message.')

    maintenance_message = models.CharField(
        max_length=160, 
        default="System is currently upgrading. Please try again later.",
        help_text="Reply sent when Active is False"
    )
    system_prompt = models.TextField(
        default=(
            "You are an offline SMS assistant. "
            "1. Answer in under 160 characters. "
            "2. Be direct. No pleasantries. "
            "3. If unsure, say 'I do not know'."
        ),
        help_text="The instruction given to OpenAI. Changes take effect immediately."
    )
    error_message = models.CharField(
        max_length=160, 
        default="Error processing request. Try again.",
        help_text="Reply sent when OpenAI fails"
    )
    default_credits = models.IntegerField(default=10, help_text="Credits given to new users")

    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"

    def __str__(self):
        return "System Configuration"


