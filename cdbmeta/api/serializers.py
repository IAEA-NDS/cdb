from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from cdbmeta import models as meta_models


class FieldConverterMixin:
    """
    This mixin class is used to convert input fields like `lattice-parameters`
    into a custom one. Because, in Python `lattice-parameters` is not a valid
    variable and hence we can not define it as a class member.

    Disclaimer:
    This is not a DRF/Django/Python feature and
    may not available in the future versions. But, it works now!!!
    """

    field_map = {}

    def normalize_fields(self):
        """
        converts non-python variables like `lattice-parameters` into a custom one
        """
        for api_field, model_field in self.field_map.items():
            self.fields[api_field] = self.fields[model_field]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize_fields()


class QualifiedIDField(serializers.Field):
    """
    This is similar to `serializers.PrimaryKeyRelatedField`,
    but, takes an alphanumeric value as input instead of an integer.

    Ex: `A123`, `B147` etc

    Parameters:
        model_cls: the Django model class to search for the row/instance
        id_prefix: optional value to indicate the model.
            If not provided, will use the first letter of the model class
        serializer: a DRF serializer class that will be used while
            serialization process
    """

    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_type": _("Incorrect type. Expected pk value, received {data_type}."),
    }

    def __init__(self, model_cls, id_prefix=None, serializer=None, **kwargs):
        kwargs.setdefault("required", False)
        self.model_cls = model_cls
        self.serializer_cls = serializer

        if id_prefix:
            self.id_prefix = id_prefix
        else:
            self.id_prefix = model_cls.__name__[0].upper()

        self._prefix_len = len(self.id_prefix)

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        pk_integer = int(data[self._prefix_len :])
        try:
            return self.model_cls.objects.get(pk=pk_integer)
        except self.model_cls.DoesNotExists:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def to_representation(self, value):
        if self.serializer_cls:
            return self.serializer_cls(value).data
        return value.pk


class AttributionSerializer(serializers.ModelSerializer):
    qid = QualifiedIDField(model_cls=meta_models.Attribution, id_prefix="A")

    class Meta:
        model = meta_models.Attribution
        fields = ["qid"]


class LatticeParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = meta_models.LatticeParameters
        fields = "__all__"


class MaterialSerializer(FieldConverterMixin, serializers.ModelSerializer):
    field_map = {
        "chemical-formula": "chemical_formula",
        "lattice-parameters": "lattice_parameters",
    }
    lattice_parameters = LatticeParameterSerializer()

    class Meta:
        model = meta_models.Material
        fields = ["chemical_formula", "structure", "lattice_parameters"]


class SimulationBoxSerializer(FieldConverterMixin, serializers.ModelSerializer):
    field_map = {
        "box-X-length": "box_X",
        "box-Y-length": "box_Y",
        "box-Z-length": "box_Z",
        "box-X-orientation": "box_X_orientation",
        "box-Y-orientation": "box_Y_orientation",
        "box-Z-orientation": "box_Z_orientation",
    }

    class Meta:
        model = meta_models.CDBRecord
        fields = [
            "box_X",
            "box_Y",
            "box_Z",
            "box_X_orientation",
            "box_Y_orientation",
            "box_Z_orientation",
        ]


class PotentialSerializer(FieldConverterMixin, serializers.ModelSerializer):
    field_map = {"source-doi": "source_doi"}
    source_doi = serializers.CharField()

    class Meta:
        model = meta_models.Potential
        fields = ["filename", "comment", "source_doi", "uri"]


class CodeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="code_name")
    version = serializers.CharField(source="code_version")

    class Meta:
        model = meta_models.CDBRecord
        fields = ["name", "version"]


class DataColumnSerializer(serializers.ModelSerializer):
    description = serializers.CharField(default="")

    class Meta:
        model = meta_models.DataColumn
        fields = ["name", "units", "description"]


class CreateMetaRecordSerializer(FieldConverterMixin, serializers.ModelSerializer):
    field_map = {
        "PKA-atomic-number": "atomic_number",
        "PKA-energy": "energy",
        "simulation-time": "total_simulation_time",
        "simulation-box": "simulation_box",
        "archive-name": "archive_name",
        "electronic-stopping": "electronic_stopping",
        "has-surface": "has_surface",
        "initial-temperature": "initial_temperature",
        "initially-perfect": "initially_perfect",
        "thermostat-comment": "thermostat_comment",
    }
    attribution = AttributionSerializer()
    material = MaterialSerializer()
    simulation_box = SimulationBoxSerializer()
    potential = PotentialSerializer()
    code = CodeSerializer()
    columns = DataColumnSerializer(many=True)

    class Meta:
        model = meta_models.CDBRecord
        fields = [
            "archive_name",
            "atomic_number",
            "attribution",
            "code",
            "columns",
            "comments",
            "electronic_stopping",
            "energy",
            "has_surface",
            "initial_temperature",
            "initially_perfect",
            "material",
            "potential",
            "recoil",
            "simulation_box",
            "thermostat",
            "thermostat_comment",
            "total_simulation_time",
        ]

    def get_or_create_related_field(
        self, validated_data: dict, field_name: str, method_name: str = None
    ):
        field_data = validated_data[field_name]
        if "qid" in field_data:
            return field_data["qid"]

        if not method_name:
            method_name = f"create_related_field_{field_name}"

        validated_data = validated_data.copy()  # be more safe
        return getattr(self, method_name)(validated_data, field_name)

    def create_related_field_lattice_parameters(
        self, validated_data: dict, field_name: str
    ):
        lattice_parameters, _ = meta_models.LatticeParameters.objects.get_or_create(
            **validated_data[field_name]
        )
        return lattice_parameters

    def create_related_field_potential(self, validated_data: dict, field_name: str):
        potential = validated_data[field_name]

        ref = None
        source_doi = potential.pop("source_doi", None)
        filename = potential.pop("filename", "")
        comment = potential.pop("comment", "")
        if source_doi:
            ref, _ = meta_models.Ref.objects.get_or_create(doi=source_doi)

        potential, _ = meta_models.Potential.objects.get_or_create(
            **potential, source=ref, filename=filename, comment=comment
        )
        return potential

    def create_related_field_material(self, validated_data: dict, field_name: str):
        material = validated_data[field_name]
        material["lattice_parameters"] = self.get_or_create_related_field(
            validated_data=material, field_name="lattice_parameters"
        )
        material, _ = meta_models.Material.objects.get_or_create(**material)
        return material

    def _create(self, validated_data):
        validated_data_copy = validated_data.copy()

        self_nested_attrs = ["simulation_box", "code"]
        for field in self_nested_attrs:
            validated_data.update(**validated_data.pop(field))

        validated_data["attribution"] = self.get_or_create_related_field(
            validated_data=validated_data_copy, field_name="attribution"
        )
        validated_data["material"] = self.get_or_create_related_field(
            validated_data=validated_data_copy, field_name="material"
        )
        validated_data["potential"] = self.get_or_create_related_field(
            validated_data=validated_data_copy, field_name="potential"
        )

        columns = validated_data.pop("columns", [])
        meta_record = meta_models.CDBRecord.objects.create(**validated_data)

        for column_data in columns:
            if column_data in meta_models.CDBRecord.DEDICATED_COLUMNS:
                continue

            data_column, _ = meta_models.DataColumn.objects.get_or_create(**column_data)
            meta_record.additional_columns.add(data_column)

        return meta_record

    def create(self, validated_data):
        with transaction.atomic():
            return self._create(validated_data=validated_data)
