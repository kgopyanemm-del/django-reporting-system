from django.db import models
from Reporting.models import Report


class StatusUpdate(models.Model):

    STATUS_CHOICES = [
        ('open',                        'Open'),
        ('issue_has_worsened',          'Issue Has Worsened'),
        ('issue_is_ongoing',            'Issue Is Ongoing'),
        ('issue_fixed',                 'Issue Fixed'),
        ('escalated_to_municipality',   'Escalated To Municipality'),
        ('scheduled_for_service',       'Scheduled For Service'),
        ('work_in_progress',            'Work In Progress'),
    ]

    report     = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='status_updates')
    new_status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    note       = models.TextField(blank=True)
    updated_by = models.CharField(max_length=100, default='System')
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report.reference_number} -> {self.get_new_status_display()}"

    class Meta:
        ordering = ['-updated_at']


class Feedback(models.Model):

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    RESOLVED_CHOICES = [
        ('yes',     'Fully Resolved'),
        ('partial', 'Partially Resolved'),
        ('no',      'Still Not Fixed'),
        ('worse',   'Made Worse'),
    ]

    report        = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='feedback')
    rating        = models.IntegerField(choices=RATING_CHOICES)
    resolved      = models.CharField(max_length=10, choices=RESOLVED_CHOICES)
    comment       = models.TextField(blank=True)
    reporter_name = models.CharField(max_length=100, blank=True)
    submitted_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.report.reference_number} — {self.rating} stars"

    class Meta:
        ordering = ['-submitted_at']


class NearbySearch(models.Model):
    latitude    = models.FloatField()
    longitude   = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search at {self.latitude}, {self.longitude}"
