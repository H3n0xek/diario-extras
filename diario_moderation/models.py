from django.db import models
from diario.models import Entry
from django.dispatch import receiver
from django.db.models.signals import post_save

STATUS_DRAFT = 0
STATUS_QUEUED = 1
STATUS_ACCEPTED = 2
STATUS_REJECTED = 3
STATUS_REWRITE = 4

MODERATION_STATUS = (
    (STATUS_DRAFT, 'draft'),
    (STATUS_QUEUED, 'queued'),
    (STATUS_ACCEPTED, 'accepted'),
    (STATUS_REJECTED, 'rejected'),
    (STATUS_REWRITE, 'rewrite')
)


class EntryStatus(models.Model):
    entry = models.ForeignKey(Entry, unique=True)
    status = models.IntegerField(choices=MODERATION_STATUS)
    comment = models.TextField(blank=True, null=True)
  

@receiver(post_save, sender=Entry)
def create_status_model(sender, instance, created, **kwargs):
    if created:
        EntryStatus.objects.create(entry=instance, status=STATUS_DRAFT)

@receiver(post_save, sender=EntryStatus)
def publish_entry(sender, instance, created, **kwargs):
    if instance.status == STATUS_ACCEPTED:
        e = instance.entry
        e.is_draft = False
        e.save()

