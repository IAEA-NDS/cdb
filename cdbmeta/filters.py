from .models import CDBRecord
import django_filters

class CDBRecordFilter(django_filters.FilterSet):

    attribution__person__name = django_filters.CharFilter(
            field_name='attribution__person__name', lookup_expr='icontains',
            label='Attribution name')
    attribution__person__institution__name = django_filters.CharFilter(
            field_name='attribution__person__institution__name',
            lookup_expr='icontains',
            label='Institution name')
    attribution__publication_doi = django_filters.CharFilter(
            field_name='attribution__publication_doi', label='Publication DOI')
    material__chemical_formula = django_filters.CharFilter(
            field_name='material__chemical_formula')
    material__structure = django_filters.CharFilter(
            field_name='material__structure')
    initial_temperature_lte = django_filters.NumberFilter(
                            field_name='initial_temperature', lookup_expr='lte')
    initial_temperature_gte = django_filters.NumberFilter(
                            field_name='initial_temperature', lookup_expr='gte')
    archive_name = django_filters.CharFilter(field_name='archive_name', 
            lookup_expr='icontains', label='Archive filename')
    energy__gte = django_filters.NumberFilter(field_name='energy',
                            lookup_expr='gte')
    energy__lte = django_filters.NumberFilter(field_name='energy',
                            lookup_expr='lte')
    potential__pk = django_filters.NumberFilter(
            field_name='potential__pk', lookup_expr='exact')


    class Meta:
        model = CDBRecord
        fields = []
