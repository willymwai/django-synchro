import django
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import models, fields
from django.db import models
from django.utils.timezone import now
import dbsettings

M2M_CHANGE = 4

ACTIONS = (
    (ADDITION, 'Add'),
    (CHANGE, 'Change'),
    (DELETION, 'Delete'),
    (M2M_CHANGE, 'M2m Change'),
)


class SynchroSettings(dbsettings.Group):
    last_check = dbsettings.DateTimeValue('Last synchronization', default=now())

options = SynchroSettings()


class Reference(models.Model):
    content_type = models.ForeignKey(ContentType)
    local_object_id = models.CharField(max_length=20)
    remote_object_id = models.CharField(max_length=20)

    class Meta:
        #app_label = 'Reference'
        unique_together = ('content_type', 'local_object_id')


class ChangeLog(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=20)
    object = fields.GenericForeignKey()
    date = models.DateTimeField(auto_now=True)
    action = models.PositiveSmallIntegerField(choices=ACTIONS)

    #class Meta:
        #app_label = 'ChangeLog'

    def __unicode__(self):
        return u'ChangeLog for %s (%s)' % (unicode(self.object), self.get_action_display())


class DeleteKey(models.Model):
    changelog = models.OneToOneField(ChangeLog)
    key = models.CharField(max_length=200)

    #class Meta:
        #app_label = 'DeleteKey'

# start logging
if django.VERSION < (1, 7):
    from signals import synchro_connect

    synchro_connect()
