from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sortedm2m.fields import SortedManyToManyField
from miniclerval.models import Person
from lxml import etree
from utils.xml import attach_element, attach_optional_element, true_false
from cdb.settings import SITE_ROOT_URL

class Attribution(models.Model):
    person = models.ForeignKey(Person)
    publication_doi = models.CharField(max_length=50)
    general_comments = models.TextField(blank=True)
    acknowledgements = models.TextField(blank=True)

    def __str__(self):
        return '{}: {}'.format(self.person.name, self.publication_doi)

    @property
    def qualified_id(self):
        return 'A{:d}'.format(self.pk)

    def cdbml(self):
        attribElement = etree.Element('attribution', id=self.qualified_id)
        nameElement = etree.SubElement(attribElement, 'name')
        nameElement.text = self.person.name
        affiliationElement = etree.SubElement(attribElement, 'affiliation')
        affiliationElement.text = self.person.institution.name
        doiElement = etree.SubElement(attribElement, 'doi')
        doiElement.text = self.publication_doi
        attach_optional_element(attribElement, 'comments',
                                self.general_comments)
        attach_optional_element(attribElement, 'acknowledgements',
                                self.acknowledgements)
        return attribElement

class LatticeParameters(models.Model):
    # The leading spaces in verbose_name are a hack to stop Django from
    # capitalizing these field names in their form labels
    a = models.FloatField(verbose_name=' a /Å')
    b = models.FloatField(verbose_name=' b /Å')
    c = models.FloatField(verbose_name=' c /Å')
    alpha = models.FloatField(verbose_name=' α /deg')
    beta = models.FloatField(verbose_name=' β /deg')
    gamma = models.FloatField(verbose_name=' γ /deg')

    class Meta:
        verbose_name_plural = 'Lattice parameters'

    def __str__(self):
        return 'a={:.3f} Å, b={:.3f} Å, c={:.3f} Å,'\
               ' α = {:.1f}°, β = {:.1f}°, γ = {:.1f}°'.format(
            self.a, self.b, self.c, self.alpha, self.beta, self.gamma)

    def cdbml(self):
        lpElement = etree.Element('lattice_parameters')
        for s_ax in 'abc':
            ax_elm = etree.SubElement(lpElement, s_ax, units='Å')
            ax_elm.text = '{:.6f}'.format(getattr(self, s_ax))
        for s_ang in ('alpha', 'beta', 'gamma'):
            ang_elm = etree.SubElement(lpElement, s_ang, units='deg')
            ang_elm.text = '{:.6f}'.format(getattr(self, s_ang))
        return lpElement


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

    def cdbml(self):
        matElement = etree.Element('material')
        formulaElement = etree.SubElement(matElement, 'formula')
        formulaElement.text = self.chemical_formula
        structureElement = etree.SubElement(matElement, 'structure')
        structureElement.text = self.structure
        matElement.append(self.lattice_parameters.cdbml())
        return matElement


class DataColumn(models.Model):
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=20, blank=True)
    description = models.TextField()

    def __str__(self):
        if self.units:
            return '{} /{}'.format(self.name, self.units)
        return self.name

class DataMixin(models.Model):
    archive_name = models.CharField(max_length=100)
    initial_configuration_filename=models.CharField(max_length=100, blank=True)
    initial_configuration_comments = models.TextField(blank=True)
    nheader = models.PositiveSmallIntegerField('Number of header rows',
                                               default=0)
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
    energy = models.FloatField('PKA energy /keV',
                               validators=[MinValueValidator(0),])
    recoil = models.BooleanField('PKA by recoil?', default=True)

    electronic_stopping = models.BooleanField(default=False)
    electronic_stopping_comment = models.CharField(max_length=500, blank=True)
    thermostat = models.BooleanField(default=False)
    thermostat_comment = models.CharField(max_length=500, blank=True)
    input_filename = models.CharField(max_length=100, blank=True)
    total_simulation_time = models.FloatField('Total simulation time /ps',
                            validators=[MinValueValidator(0),])
    initial_temperature = models.FloatField('Initial temperature /K',
                                            validators=[MinValueValidator(0),])
    interatomic_potential_filename = models.CharField(max_length=100,
                                                      blank=True)
    interatomic_potential_comment = models.TextField(blank=True)
    code_name = models.CharField(max_length=100)
    code_version = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'CDB record'
        verbose_name_plural = 'CDB records'

    def __str__(self):
        return '{}: {} ({}), {} eV; {} ps: {}'.format(
            self.attribution.person.name,
            self.material.chemical_formula, self.material.structure,
            self.energy, self.total_simulation_time, self.archive_name)

    @property
    def qualified_id(self):
        return 'R{:d}'.format(self.pk)

    def cdbml(self):
        cdbrecordElement = etree.Element('cdbrecord', id=self.qualified_id)
        cdbrecordElement.append(self.attribution.cdbml())
        cdbrecordElement.append(self.material.cdbml())
        attach_element(cdbrecordElement, 'has_surface', self.has_surface,
                      true_false)
        attach_element(cdbrecordElement, 'initially_perfect',
                       self.initially_perfect, true_false)
        attach_element(cdbrecordElement, 'PKA_atomic_number',
                       self.atomic_number, '{:d}')
        PKAElement = etree.SubElement(cdbrecordElement, 'PKA')
        attach_element(PKAElement, 'energy',
                       self.energy, '{:f}', attrs={'units': 'keV'})
        attach_element(PKAElement, 'recoil',
                       self.recoil, true_false)
        attach_element(cdbrecordElement, 'electronic_stopping',
                       self.electronic_stopping, true_false)
        attach_optional_element(cdbrecordElement,'electronic_stopping_comment',
                        self.electronic_stopping_comment)
        attach_element(cdbrecordElement, 'thermostat',
                       self.thermostat, true_false)
        attach_optional_element(cdbrecordElement,'thermostat_comment',
                        self.thermostat_comment)
        attach_optional_element(cdbrecordElement, 'input_filename',
                        self.input_filename)
        attach_element(cdbrecordElement, 'simulation_time',
                   self.total_simulation_time, '{:.3f}', attrs={'units': 'ps'})
        attach_element(cdbrecordElement, 'initial_temperature',
                   self.initial_temperature, '{:.2f}', attrs={'units': 'K'})
        if (self.interatomic_potential_filename or
            self.interatomic_potential_comment):
            PEElement = etree.SubElement(cdbrecordElement,
                                         'interatomic_potential')
            attach_optional_element(PEElement, 'filename',
                           self.interatomic_potential_filename)
            attach_optional_element(PEElement, 'comment',
                           self.interatomic_potential_comment)
        codeElement = etree.SubElement(cdbrecordElement, 'code')
        attach_element(codeElement, 'name', self.code_name)
        attach_element(codeElement, 'version', self.code_version)
        if (self.initial_configuration_filename or
                    self.initial_configuration_comments):
            initial_configElement = etree.SubElement(cdbrecordElement,
                                                     'initial_configuration')
            attach_optional_element(initial_configElement, 'filename',
                                    self.initial_configuration_filename)
            attach_optional_element(initial_configElement, 'comments',
                                    self.initial_configuration_comments)
        dataElement = etree.SubElement(cdbrecordElement, 'data')
        attach_element(dataElement, 'archive_name', self.archive_name)
        attach_element(dataElement, 'nheader', self.nheader, '{:d}')
        colsElement = etree.SubElement(dataElement, 'columns')

        def column_element(name, units=None, description=None):
            colElement = etree.Element('column')
            attach_element(colElement, 'name', name)
            attach_optional_element(colElement, 'units', units)
            attach_optional_element(colElement, 'description', description)
            return colElement

        colsElement.append(column_element('Element Symbol'))
        colsElement.append(column_element('x', 'Å'))
        colsElement.append(column_element('y', 'Å'))
        colsElement.append(column_element('z', 'Å'))
        for column in self.additional_columns.all():
            colsElement.append(column_element(column.name,
                                    column.units, column.description))

        return cdbrecordElement

    def as_cdbml(self, standalone=True, xml2html=False):
        cdbml = etree.tostring(self.cdbml(), pretty_print=True,
                               encoding='unicode')

        if not standalone:
            return cdbml

        s = ['<?xml version="1.0" encoding="utf-8" ?>']

        if xml2html:
            s.append('<?xml-stylesheet type="text/xsl" href='
                     '"{}/static/xsl/cdbml2html.xsl"?>'.format(SITE_ROOT_URL))
        s.extend([
            '<cdbml version="1.0" xmlns="https://www-amdis.iaea.org/cdbml">',
            cdbml,
            '</cdbml>'])
            
        return '\n'.join(s)
