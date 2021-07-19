from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sortedm2m.fields import SortedManyToManyField
from miniclerval.models import Person
from refs.models import Ref
import json
from lxml import etree
from utils.serialize_utils import add_optional_kv
from utils.xml import attach_element, attach_optional_element, true_false
from django.conf import settings

class Attribution(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    source = models.ForeignKey(Ref, blank=True, null=True,
                               on_delete=models.CASCADE)
    general_comments = models.TextField(blank=True)
    acknowledgements = models.TextField(blank=True)

    def __str__(self):
        return '{}: {}'.format(self.person.name, self.publication_doi)


    @property
    def publication_doi(self):
        try:
            return self.source.doi or '[No DOI]'
        except AttributeError:
            return '[No source Ref]'

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

    def serialize(self):
        d = {'qid': self.qualified_id}
        add_optional_kv(d, 'contact', self, 'person', 'serialize')
        add_optional_kv(d, 'source_doi', self.source, 'doi')
        add_optional_kv(d, 'source_url', self.source, 'url')
        add_optional_kv(d, 'general-comments', self)
        add_optional_kv(d, 'acknowledgements', self)
        return d
        

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
        return 'a={:.10g} Å, b={:.10g} Å, c={:.10g} Å,'\
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

    def serialize(self):
        d = {'a': self.a, 'b': self.b, 'c': self.c,
             'alpha': self.alpha, 'beta': self.beta, 'gamma': self.gamma}
        return d


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
                           blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        s = '{} ({})'.format(self.chemical_formula, self.structure)
        if self.lattice_parameters:
            return '{}: {}'.format(s, self.lattice_parameters)
        return s

    def cdbml(self):
        matElement = etree.Element('material')
        formulaElement = etree.SubElement(matElement, 'formula')
        formulaElement.text = self.chemical_formula
        structureElement = etree.SubElement(matElement, 'structure')
        structureElement.text = self.structure
        matElement.append(self.lattice_parameters.cdbml())
        return matElement

    def serialize(self):
        d = {'chemical-formula': self.chemical_formula,
             'structure': self.structure,
             'lattice-parameters': self.lattice_parameters.serialize(),
            }
        return d

class Potential(models.Model):
    filename = models.CharField(max_length=100,
        help_text='If provided, the filename or URL to a resource providing '
            'the interatomic potential(s) used in the simulation', blank=True)
    comment = models.TextField(blank=True)
    source = models.ForeignKey(Ref, blank=True, null=True,
                               on_delete=models.CASCADE)

    @property
    def qualified_id(self):
        return 'P{}'.format(self.id)

    @property
    def uri(self):
        return settings.POTENTIAL_URI_STEM + '/' + str(self.pk)

    def link(self):
        return '<a href="{}/{}">{}</a>'.format('potential', self.pk,
                                               self.qualified_id)

    def __str__(self):
        s = '{}:'.format(self.qualified_id)
        if self.filename:
            s = s + ' ' + str(self.filename) 
        if self.source:
            return s + ' ({})'.format(self.source)
        return s + ' [missing ref]'

    def serialize(self):
        d = {}
        add_optional_kv(d, 'filename', self)
        add_optional_kv(d, 'comment', self)
        add_optional_kv(d, 'source-doi', self.source, 'doi')
        add_optional_kv(d, 'uri', self)
        return d


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
    archive_filesize = models.BigIntegerField(
                validators=[MinValueValidator(0),], blank=True, null=True)
    nsim = models.PositiveSmallIntegerField(null=True, blank=True,
                verbose_name='Number of simulations')
    initial_configuration_filename=models.CharField(max_length=100, blank=True,
        help_text='If provided, the filename of the .xyz file giving the '
                  'initial state of the material in the simulation')
    initial_configuration_comments = models.TextField(blank=True)
    additional_columns = SortedManyToManyField(DataColumn, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        abstract=True
        verbose_name_plural = 'Data'


class CDBRecord(DataMixin):
    DEDICATED_COLUMNS = [
        {'name': 'Element Symbol'},
        {'name': 'x', 'units': 'Å'},
        {'name': 'y', 'units': 'Å'},
        {'name': 'z', 'units': 'Å'},
    ]
    attribution = models.ForeignKey(Attribution,
        help_text='Person, publication DOI, comments and acknowledgements',
        on_delete=models.CASCADE)
    material = models.ForeignKey(Material,
        help_text='Chemical formula, structure and lattice parameters',
        on_delete=models.CASCADE)
    has_surface = models.BooleanField('Does the simulation include a surface?',
                                      default=False)
    initially_perfect = models.BooleanField(
                'Is the crystal initially perfect?', default=True)

    atomic_number = models.PositiveSmallIntegerField(
        'Projectile / PKA atomic number',
        validators=[MinValueValidator(1), MaxValueValidator(118)],
        help_text='Example: 74 [for a tungsten PKA]')
    energy = models.FloatField('Projectile / PKA energy /keV',
                               validators=[MinValueValidator(0),])
    recoil = models.BooleanField('PKA by recoil?', default=True)

    electronic_stopping = models.BooleanField(
                'Is electronic stopping included?', default=False)
    electronic_stopping_comment = models.CharField(max_length=500, blank=True)
    thermostat = models.BooleanField('Is a thermostat included?',
                default=False)
    thermostat_comment = models.CharField(max_length=500, blank=True)
    input_filename = models.CharField(max_length=100, blank=True,
        help_text='The input filename(s) (or filename pattern) for the MD '
                  'simulation code; separate multiple filenames by whitespace')
    total_simulation_time = models.FloatField('Total simulation time /ps',
                            validators=[MinValueValidator(0),])
    initial_temperature = models.FloatField('Initial temperature /K',
                                            validators=[MinValueValidator(0),])

    box_X = models.FloatField('Box X-length /Å',
                              validators=[MinValueValidator(0),])
    box_Y = models.FloatField('Box Y-length /Å',
                              validators=[MinValueValidator(0),])
    box_Z = models.FloatField('Box Z-length /Å',
                              validators=[MinValueValidator(0),])
    box_X_orientation = models.CharField('Box X-orientation', max_length=15,
            help_text='As Miller indices, e.g. (100)', blank=True)
    box_Y_orientation = models.CharField('Box Y-orientation', max_length=15,
            help_text='As Miller indices, e.g. (010)', blank=True)
    box_Z_orientation = models.CharField('Box Z-orientation', max_length=15,
            help_text='As Miller indices, e.g. (001)', blank=True)

    potential = models.ForeignKey(Potential, blank=True, null=True,
                                  on_delete=models.CASCADE)
    code_name = models.CharField(max_length=100, help_text='e.g. "LAMMPS"')
    code_version = models.CharField(max_length=20,
        help_text='e.g. "22 Aug 2018"')

    class Meta:
        verbose_name = 'CDB record'
        verbose_name_plural = 'CDB records'

    def __str__(self):
        return '{}: {} ({}), {} keV; {} ps: {}'.format(
            self.attribution.person.name,
            self.material.chemical_formula, self.material.structure,
            self.energy, self.total_simulation_time, self.archive_name)

    @property
    def qualified_id(self):
        return 'R{:03x}'.format(self.pk)

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

        simulation_box_element = etree.SubElement(cdbrecordElement,
                                                        'simulation_box')
        attach_element(simulation_box_element, 'box_X_length', self.box_X,
                       '{:.4f}', attrs={'units': 'Å'})
        attach_element(simulation_box_element, 'box_Y_length', self.box_Y,
                       '{:.4f}', attrs={'units': 'Å'})
        attach_element(simulation_box_element, 'box_Z_length', self.box_Z,
                       '{:.4f}', attrs={'units': 'Å'})
        if any((self.box_X_orientation, self.box_Y_orientation,
                                            self.box_Z_orientation)):
            box_orientation_element = etree.SubElement(simulation_box_element,
                                                       'box_orientation')
            attach_element(box_orientation_element, 'X_orientation',
                           self.box_X_orientation or 'MISSING')
            attach_element(box_orientation_element, 'Y_orientation',
                           self.box_Y_orientation or 'MISSING')
            attach_element(box_orientation_element, 'Z_orientation',
                           self.box_Z_orientation or 'MISSING')

        if self.potential:
            PEElement = etree.SubElement(cdbrecordElement,
                                         'interatomic_potential')
            attach_optional_element(PEElement, 'uri', self.potential.uri)
            if (self.potential.filename or self.potential.comment or
                    self.potential.source):
                attach_optional_element(PEElement, 'filename',
                               self.potential.filename)
                attach_optional_element(PEElement, 'comment',
                               self.potential.comment)
                if self.potential.source:
                    attach_optional_element(PEElement, 'doi',
                                   self.potential.source.doi)
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
        colsElement = etree.SubElement(dataElement, 'columns')
        attach_optional_element(dataElement, 'comments',
                                self.comments)

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

    def as_cdbml(self, standalone=True, xsl_name=None):
        cdbml = etree.tostring(self.cdbml(), pretty_print=True,
                               encoding='unicode')

        if not standalone:
            return cdbml

        s = ['<?xml version="1.0" encoding="utf-8" ?>']

        if xsl_name:
            s.append('<?xml-stylesheet type="text/xsl" href='
                     '"{}/static/xsl/{}"?>'.format(settings.SITE_ROOT_URL,
                                                   xsl_name))
        s.extend([
            '<cdbml version="1.0" xmlns="https://amdis.iaea.org/cdbml">',
            cdbml,
            '</cdbml>'])
            
        return '\n'.join(s)

    def serialize(self):
        d = {'qid': self.qualified_id,
             'attribution': self.attribution.serialize(),
             'material': self.material.serialize(),
             'potential': self.potential.serialize(),
            }
        add_optional_kv(d, 'has-surface', self)
        add_optional_kv(d, 'initially-perfect', self)
        add_optional_kv(d, 'PKA-atomic-number', self, 'atomic_number')
        add_optional_kv(d, 'PKA-energy', self, 'energy')
        add_optional_kv(d, 'recoil', self)
        add_optional_kv(d, 'electronic-stopping', self)
        add_optional_kv(d, 'electronic-stopping-comment', self)
        add_optional_kv(d, 'thermostat', self)
        add_optional_kv(d, 'thermostat-comment', self)
        add_optional_kv(d, 'input-filename', self)
        add_optional_kv(d, 'simulation-time', self, 'total_simulation_time')
        add_optional_kv(d, 'initial-temperature', self)

        dbox = {}
        add_optional_kv(dbox, 'box-X-length', self, 'box_X')
        add_optional_kv(dbox, 'box-Y-length', self, 'box_Y')
        add_optional_kv(dbox, 'box-Z-length', self, 'box_Z')
        add_optional_kv(dbox, 'box-X-orientation', self, 'box_X_orientation')
        add_optional_kv(dbox, 'box-Y-orientation', self, 'box_Y_orientation')
        add_optional_kv(dbox, 'box-Z-orientation', self, 'box_Z_orientation')
        d['simulation-box'] = dbox

        dcolumns = self.DEDICATED_COLUMNS.copy()  # This is being reused in serializer
        for column in self.additional_columns.all():
            dcolumn = {'name': column.name}
            add_optional_kv(dcolumn, 'units', column)
            add_optional_kv(dcolumn, 'description', column)
            dcolumns.append(dcolumn)
        d['columns'] = dcolumns

        d['code'] = {'name': self.code_name, 'version': self.code_version}
        d['archive-name'] = self.archive_name
        add_optional_kv(d, 'archive_filesize', self)
        add_optional_kv(d, 'number-of-simulations', self, 'nsim')
        add_optional_kv(d, 'initial-configuration-filename', self)
        add_optional_kv(d, 'initial-configuration-comments', self)
        add_optional_kv(d, 'comments', self)

        return d

    def as_json(self):
        return json.dumps(self.serialize())
