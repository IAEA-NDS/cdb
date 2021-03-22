from rest_framework import serializers
from .models import Institution, Person
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

#class jInstitutionSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    name = serializers.CharField(max_length=500)
#    country = CountryField()
#
#    def create(self, validated_data):
#        """
#        Create and return a new `Institution` instance, given validated data.
#        """
#        return Institution.objects.create(**validated_data)
#
#
#    def update(self, instance, validated_data):
#        """
#        Update and return an existing `Institution` instance, given the
#        validated data.
#
#        """
#
#        instance.name = validated_data.get('name', instance.name)
#        instance.country = validated_data.get('country', instance.country)
#        instance.save()
#        return instance

class QualifiedIdMixin:
    def get_qid(self, obj):
        """Called by serializers.SerializerMethodField called qid."""
        return obj.qualified_id
    

class InstitutionSerializer(CountryFieldMixin, serializers.ModelSerializer,
                            QualifiedIdMixin):

    qid = serializers.SerializerMethodField(required=False)
    name = serializers.CharField(max_length=500, required=False)
    country = CountryField(required=False)

    class Meta:
        model = Institution
        fields = ('qid', 'name', 'country')

    def to_internal_value(self, data):
        if type(data) == str:
            institution_id = data
            if institution_id.startswith(Institution.QPREFIX):
                institution_id = institution_id[len(Institution.QPREFIX):]
            institution = Institution.objects.get(id=institution_id)
            return InstitutionSerializer(institution)
        return super().to_internal_value(data)



class PersonSerializer(serializers.ModelSerializer, QualifiedIdMixin):

    qid = serializers.SerializerMethodField(required=False)
    name = serializers.CharField(max_length=100, required=False)
    institution = InstitutionSerializer(many=False, required=False)
    

    class Meta:
        model = Person
        fields = ('qid', 'name', 'institution', 'email', 'url')


    def to_internal_value(self, data):
        if type(data) == str:
            person_id = data
            if person_id.startswith(Person.QPREFIX):
                person_id = person_id[len(Person.QPREFIX):]
            person = Person.objects.get(id=person_id)
            return PersonSerializer(person)
        return super().to_internal_value(data)

    def qvalidate(self, data):
        # 'qid' is missing from data because it comes from SeralizerMethodField
        qid = self.initial_data.get('qid')
        if qid is None:
            name = data.get('name')
            if name is None:
                raise serializers.ValidationError({'name': ['name is a'
                    ' required field if qid is not provided.']})
        else:
            # Inject the qid into the validated data.
            data['qid'] = qid
        return data 
