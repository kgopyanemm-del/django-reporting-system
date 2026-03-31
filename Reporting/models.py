from django.db import models

class Report(models.Model):

    CATEGORY_CHOICES = [
        ('streetlight',         'Streetlight'),
        ('water_leaks',         'Water Leaks'),
        ('waste_sanitation',    'Waste & Sanitation'),
        ('roads_potholes',      'Roads & Potholes'),
        ('environment_health',  'Environment & Public Health'),
        ('parks_biodiversity',  'Parks, Trees & Biodiversity'),
        ('electricity',         'Electricity'),
    ]

    SUB_ISSUE_CHOICES = [
        ('light_not_working',   'Light Not Working'),
        ('light_fitting',       'Light Fitting Missing/Stolen'),
        ('cable_theft',         'Cable Theft From Pole'),
        ('pole_damage',         'Pole Damage'),
        ('light_on',            'Light On During Day'),
        ('water_pipe',          'Water Pipe Damaged/Leaking'),
        ('water_meter',         'Water Meter Damage'),
        ('water_outage',        'Localised Water Outage'),
        ('sewerage_leak',       'Sewerage Leak'),
        ('illegal_dumping',     'Illegal Dumping'),
        ('storm_drain',         'Storm Drain Blocked'),
        ('missed_collection',   'Missed Collection Day'),
        ('overflowing_bin',     'Overflowing Bin'),
        ('pothole',             'Pothole'),
        ('sinkhole',            'Sinkhole'),
        ('road_markings',       'Faded Road Markings'),
        ('traffic_sign',        'Traffic Sign Damaged'),
        ('pavement_damaged',    'Pavement Damaged'),
        ('hazardous_waste',     'Hazardous Waste'),
        ('water_pollution',     'Water Pollution'),
        ('sewage_outfalls',     'Sewage Into Rivers'),
        ('oil_spill',           'Oil/Fuel Spill'),
        ('asbestos_exposure',   'Asbestos Exposure'),
        ('illegal_trading',     'Illegal Trading'),
        ('trees',               'Fallen Tree/Dangerous Branches'),
        ('maintenance',         'Overgrown Verge/Park Maintenance'),
        ('tree_felling',        'Illegal Tree Felling'),
        ('playground',          'Playground Equipment Broken'),
        ('electricity_outage',  'Localised Electricity Outage'),
        ('illegal_connection',  'Illegal Connection Suspected'),
        ('substation_fault',    'Substation Fault Suspected'),
        ('exposed_cable',       'Exposed Live Cable'),
        ('traffic_lights',      'Traffic Lights Broken'),
    ]

    STATUS_CHOICES = [
        ('open',                        'Open'),
        ('issue_has_worsened',          'Issue Has Worsened'),
        ('issue_is_ongoing',            'Issue Is Ongoing'),
        ('issue_fixed',                 'Issue Fixed'),
        ('escalated_to_municipality',   'Escalated To Municipality'),
        ('scheduled_for_service',       'Scheduled For Service'),
        ('work_in_progress',            'Work In Progress'),
    ]

    MUNICIPALITY_CHOICES = [
        ('COJ',  'City of Johannesburg'),
        ('COT',  'City of Tshwane'),
        ('EKU',  'Ekurhuleni'),
        ('CoCT', 'City of Cape Town'),
        ('ETH',  'eThekwini'),
        ('NMB',  'Nelson Mandela Bay'),
        ('MAN',  'Mangaung'),
        ('BUF',  'Buffalo City'),
        ('OTHER','Other'),
    ]

    category         = models.CharField(max_length=30,  choices=CATEGORY_CHOICES)
    sub_issue        = models.CharField(max_length=30,  choices=SUB_ISSUE_CHOICES, blank=True)
    description      = models.TextField()
    location         = models.CharField(max_length=255)
    latitude         = models.FloatField(null=True, blank=True)
    longitude        = models.FloatField(null=True, blank=True)
    municipality     = models.CharField(max_length=10,  choices=MUNICIPALITY_CHOICES, blank=True)
    status           = models.CharField(max_length=30,  choices=STATUS_CHOICES, default='open')
    reporter_name    = models.CharField(max_length=100, blank=True)
    whatsapp_number  = models.CharField(max_length=20,  blank=True)
    reference_number = models.CharField(max_length=20,  unique=True, blank=True)
    photo            = models.ImageField(upload_to='reports/', null=True, blank=True)
    submitted_at     = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference_number:
            import random
            self.reference_number = 'CF-' + str(random.randint(1000, 9999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} | {self.get_category_display()} — {self.location}"

    class Meta:
        ordering = ['-submitted_at']
