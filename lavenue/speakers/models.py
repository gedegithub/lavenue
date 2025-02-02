from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
	ROLE_PRESIDENT = "p"
	ROLE_SECRETARY = "s"
	ROLE_MEMBER = "m"
	ROLE_CHOICES = (
		(ROLE_PRESIDENT, _("president")),
		(ROLE_SECRETARY, _("secretary")),
		(ROLE_MEMBER, _("member")),
	)

	meeting = models.ForeignKey('organisations.Meeting', models.CASCADE, verbose_name=_("meeting"))
	name = models.CharField(max_length=100, verbose_name=_("name"))

	# Need to protect the model to prevent changes in previous meetings
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, verbose_name=_("user"))
	role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=ROLE_MEMBER, verbose_name=_("role"))

	voting = models.BooleanField(default=False, verbose_name=_("voting"))
	speaking = models.BooleanField(default=False, verbose_name=_("speaking"))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("participant")
		verbose_name_plural = _("participants")

		unique_together = (('meeting', 'user'),)


class Intervention(models.Model):
	participant = models.ForeignKey(Participant, models.PROTECT, verbose_name=_("participant"))
	point = models.ForeignKey('organisations.Point', models.CASCADE, verbose_name=_("point"))
	motion = models.ForeignKey('motions.Motion', models.CASCADE, blank=True, null=True, verbose_name=_("motion"))

	time_asked = models.CharField(max_length=100, verbose_name=_("time asked"))
	time_granted = models.CharField(max_length=100, verbose_name=_("time granted"))
	seq = models.PositiveIntegerField(verbose_name=("sequence number"))

	summary = models.TextField(blank=True, verbose_name=_("summary"))

	def __str__(self):
		return "%s: %s (%d)" % (self.participant, self.point, self.seq)

	class Meta:
		verbose_name = _("intervention")
		verbose_name_plural = _("interventions")

		unique_together = (('point', 'motion', 'seq'),)
