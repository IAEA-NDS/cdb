from django.db import models
from django_countries.fields import CountryField
from utils.mixins import SerializableModel
from utils.serialize_utils import add_optional_kv

class Institution(SerializableModel):
    """A class representing a physical research institution.

    A research institution in this context may be a university, university
    department, research institute, company, etc... involved in research.
    It will usually have a single geographic location and a website.

    """

    QPREFIX = 'I'

    # These are the fixed types of institution recognised by clerval.
    INSTITUTION_CHOICES = (
               ('UNIVERSITY', 'University'),
               ('UNIVERSITY DEPARTMENT', 'University Department'),
               ('RESEARCH INSTITUTE', 'Research Institute'),
               ('COMPANY', 'Company'),
               ('INTERNATIONAL ORGANISATION', 'International Organisation'),
                          )

    name = models.CharField(max_length=500)
    country = CountryField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True)
    notes = models.TextField(max_length=4000, blank=True)
    wikipedia = models.URLField(blank=True)
    url = models.URLField(blank=True)
    institution_type = models.CharField(max_length=50,
                                choices=INSTITUTION_CHOICES, blank=True)
    address = models.CharField(max_length=1000, blank=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    def serialize(self):
        d = {'qid': self.qualified_id, 'name': self.name,
             'country': str(self.country.name)}
        return d


class Person(SerializableModel):
    """A class representing an individual researcher."""

    name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, null=True, blank=True,
                                    on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    notes = models.TextField(max_length=4000, blank=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    @property
    def surname(self):
        """Extract the surname from the Person's full name."""

        name_parts = self.name.split()
        surname_parts = []
        for name in name_parts:
            if '.' in name:
                # Skip initials
                continue
            if not name.isupper():
                continue
            if len(name) == 1:
                # Skip single-letter components
                continue
            # Capitalize the surname fragments, but look out for special cases
            name = name.title()
            if name == 'Van':
                name = 'van'
            surname_parts.append(name)
        
        surname = ' '.join(surname_parts)
        return surname

    def serialize(self):
        d = {'qid': self.qualified_id, 'name': self.name}
        add_optional_kv(d, 'institution', self, 'institution',
                        'serialize') 
        add_optional_kv(d, 'email', self)
        add_optional_kv(d, 'url', self)
        return d
