from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sortedm2m.fields import SortedManyToManyField

class Attribution(models.Model):
    name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=500)
    publication_doi = models.CharField(max_length=50)
    general_comments = models.TextField(blank=True)
    acknowledgements = models.TextField(blank=True)

    def __str__(self):
        return self.name


class LatticeParameters(models.Model):
    a = models.FloatField(verbose_name='a /Å')
    b = models.FloatField(verbose_name='b /Å')
    c = models.FloatField(verbose_name='c /Å')
    alpha = models.FloatField(verbose_name='α /deg')
    beta = models.FloatField(verbose_name='β /deg')
    gamma = models.FloatField(verbose_name='γ /deg')

    class Meta:
        verbose_name_plural = 'Lattice parameters'

    def __str__(self):
        return 'a={:.3f} Å, b={:.3f} Å, c={:.3f} Å,'\
               ' α = {:.1f}°, β = {:.1f}°, γ = {:.1f}°'.format(
            self.a, self.b, self.c, self.alpha, self.beta, self.gamma)


class Material(models.Model):

    # These are the structure types recognised by CascadeDB
    FCC, BCC, HCP, DIA, AMO, OTHER = ('fcc', 'bcc', 'hcp', 'dia',
                                      'amorphous', 'other')
    STRUCTURE_CHOICES = (
        (FCC, 'face-centred cubic'),
        (BCC, 'body-centred cubic'),
        (HCP, 'hexagonal close packed'),
        (DIA, 'diamond'),
        (AMO, 'amorphous'),
        (OTHER, 'other'),
    )

    chemical_formula = models.CharField(max_length=100)
    structure = models.CharField(max_length=100, choices=STRUCTURE_CHOICES)
    lattice_parameters = models.OneToOneField(LatticeParameters,
                                           blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.chemical_formula, self.structure)


class DataColumn(models.Model):
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=20, blank=True)
    description = models.TextField()

    def __str__(self):
        if self.units:
            return '{} /{}'.format(self.name, self.units)
        return self.name

class DataMixin(models.Model):
    filename = models.CharField(max_length=100)
    initial_configuration_filename=models.CharField(max_length=100, blank=True)
    initial_configuration_comments = models.TextField(blank=True)
    additional_columns = SortedManyToManyField(DataColumn, blank=True)

    class Meta:
        abstract=True
        verbose_name_plural = 'Data'

class CDBRecord(DataMixin):
    attribution = models.ForeignKey(Attribution)
    material = models.ForeignKey(Material)
    has_surface = models.BooleanField(default=False)
    initially_perfect = models.BooleanField(default=True)

    atomic_number = models.PositiveSmallIntegerField('PKA atomic number',
        validators=[MinValueValidator(1), MaxValueValidator(118)])
    energy = models.FloatField('PKA energy /eV',
                               validators=[MinValueValidator(0),])
    recoil = models.BooleanField('PKA by recoil?', default=True)

    electronic_stopping = models.BooleanField(default=False)
    electronic_stopping_comment = models.CharField(max_length=500, blank=True)
    thermostat = models.BooleanField(default=False)
    thermostat_stopping_comment = models.CharField(max_length=500, blank=True)
    total_simulation_time = models.FloatField('Total simulation time /ps',
                            validators=[MinValueValidator(0),])
    initial_temperature = models.FloatField(validators=[MinValueValidator(0),])
    interatomic_potential_filename = models.CharField(max_length=100)
    interatomic_potential_comment = models.TextField(blank=True)
    code_name = models.CharField(max_length=100)
    code_version = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'CDB record'
        verbose_name_plural = 'CDB records'

    def __str__(self):
        return '{}: {} ({}), {} eV; {} ps: {}'.format(self.attribution.name,
            self.material.chemical_formula, self.material.structure,
            self.energy, self.total_simulation_time, self.filename)
