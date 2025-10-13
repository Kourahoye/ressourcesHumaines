from django.db.models.signals import post_save
from django.dispatch import receiver
from Accounts.models import Article


@receiver(post_save, sender=Article)
def my_handler(sender,**kwargs):
    print("=================================================================================")