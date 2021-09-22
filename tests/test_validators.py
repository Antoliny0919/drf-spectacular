from datetime import timedelta
from unittest import mock

import jsonschema
import pytest
from django.core import validators
from django.urls import path
from rest_framework import serializers
from rest_framework.decorators import api_view

from drf_spectacular.utils import extend_schema
from tests import assert_schema, generate_schema


@mock.patch('rest_framework.settings.api_settings.COERCE_DECIMAL_TO_STRING', False)
def test_validators():

    class XSerializer(serializers.Serializer):
        # Note that these fields intentionally use basic field types to ensure that we detect from the validator only.

        # The following only apply for `string` type:
        char_email = serializers.CharField(validators=[validators.EmailValidator()])
        char_url = serializers.CharField(validators=[validators.URLValidator()])
        char_regex = serializers.CharField(validators=[validators.RegexValidator(r'\w+')])
        char_max_length = serializers.CharField(validators=[validators.MaxLengthValidator(200)])
        char_min_length = serializers.CharField(validators=[validators.MinLengthValidator(100)])

        # The following only apply for `integer` and `number` types:
        float_max_value = serializers.FloatField(validators=[validators.MaxValueValidator(200.0)])
        float_min_value = serializers.FloatField(validators=[validators.MinValueValidator(100.0)])
        float_decimal = serializers.FloatField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )
        integer_max_value = serializers.IntegerField(validators=[validators.MaxValueValidator(200)])
        integer_min_value = serializers.IntegerField(validators=[validators.MinValueValidator(100)])
        integer_decimal = serializers.FloatField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )
        decimal_max_value = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.MaxValueValidator(200)],
        )
        decimal_min_value = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.MinValueValidator(100)],
        )
        decimal_decimal = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

        # The following only apply for `array` type:
        list_max_length = serializers.ListField(validators=[validators.MaxLengthValidator(200)])
        list_min_length = serializers.ListField(validators=[validators.MinLengthValidator(100)])

        # Explicit test for rest_framework.fields.DurationField:
        age = serializers.DurationField(validators=[
            validators.RegexValidator(r'^P\d+Y$'),
            validators.MaxLengthValidator(5),
            validators.MinLengthValidator(3),
        ])

    class YSerializer(serializers.Serializer):
        # These validators are unsupported for the `string` type:
        char_max_value = serializers.CharField(validators=[validators.MaxValueValidator(200)])
        char_min_value = serializers.CharField(validators=[validators.MinValueValidator(100)])
        char_decimal = serializers.CharField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

        # These validators are unsupported for the `integer` and `number` types:
        float_email = serializers.FloatField(validators=[validators.EmailValidator()])
        float_url = serializers.FloatField(validators=[validators.URLValidator()])
        float_regex = serializers.FloatField(validators=[validators.RegexValidator(r'\w+')])
        float_max_length = serializers.FloatField(validators=[validators.MaxLengthValidator(200)])
        float_min_length = serializers.FloatField(validators=[validators.MinLengthValidator(100)])
        integer_email = serializers.IntegerField(validators=[validators.EmailValidator()])
        integer_url = serializers.IntegerField(validators=[validators.URLValidator()])
        integer_regex = serializers.IntegerField(validators=[validators.RegexValidator(r'\w+')])
        integer_max_length = serializers.IntegerField(validators=[validators.MaxLengthValidator(200)])
        integer_min_length = serializers.IntegerField(validators=[validators.MinLengthValidator(100)])
        decimal_email = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.EmailValidator()],
        )
        decimal_url = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.URLValidator()],
        )
        decimal_regex = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.RegexValidator(r'\w+')],
        )
        decimal_max_length = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.MaxLengthValidator(200)],
        )
        decimal_min_length = serializers.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[validators.MinLengthValidator(100)],
        )

        # These validators are unsupported for the `array` type:
        list_email = serializers.ListField(validators=[validators.EmailValidator()])
        list_url = serializers.ListField(validators=[validators.URLValidator()])
        list_regex = serializers.ListField(validators=[validators.RegexValidator(r'\w+')])
        list_max_value = serializers.ListField(validators=[validators.MaxValueValidator(200)])
        list_min_value = serializers.ListField(validators=[validators.MinValueValidator(100)])
        list_decimal = serializers.ListField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

        # These validators are unsupported for the `object` type:
        dict_email = serializers.DictField(validators=[validators.EmailValidator()])
        dict_url = serializers.DictField(validators=[validators.URLValidator()])
        dict_regex = serializers.DictField(validators=[validators.RegexValidator(r'\w+')])
        dict_max_length = serializers.DictField(validators=[validators.MaxLengthValidator(200)])
        dict_min_length = serializers.DictField(validators=[validators.MinLengthValidator(100)])
        dict_max_value = serializers.DictField(validators=[validators.MaxValueValidator(200)])
        dict_min_value = serializers.DictField(validators=[validators.MinValueValidator(100)])
        dict_decimal = serializers.DictField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

        # These validators are unsupported for the `boolean` type:
        boolean_email = serializers.BooleanField(validators=[validators.EmailValidator()])
        boolean_url = serializers.BooleanField(validators=[validators.URLValidator()])
        boolean_regex = serializers.BooleanField(validators=[validators.RegexValidator(r'\w+')])
        boolean_max_length = serializers.BooleanField(validators=[validators.MaxLengthValidator(200)])
        boolean_min_length = serializers.BooleanField(validators=[validators.MinLengthValidator(100)])
        boolean_max_value = serializers.BooleanField(validators=[validators.MaxValueValidator(200)])
        boolean_min_value = serializers.BooleanField(validators=[validators.MinValueValidator(100)])
        boolean_decimal = serializers.BooleanField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

        # Explicit test for rest_framework.fields.DurationField:
        duration_max_value = serializers.DurationField(validators=[validators.MaxValueValidator(200)])
        duration_min_value = serializers.DurationField(validators=[validators.MinValueValidator(100)])
        duration_decimal = serializers.DurationField(
            validators=[validators.DecimalValidator(max_digits=4, decimal_places=2)],
        )

    @extend_schema(request=XSerializer, responses=XSerializer)
    @api_view(['POST'])
    def view_func_x(request, format=None):
        pass  # pragma: no cover

    @extend_schema(request=YSerializer, responses=YSerializer)
    @api_view(['POST'])
    def view_func_y(request, format=None):
        pass  # pragma: no cover

    assert_schema(
        generate_schema(None, patterns=[path('x', view_func_x), path('y', view_func_y)]),
        'tests/test_validators.yml'
    )


@pytest.mark.xfail
def test_nested_validators():
    class XSerializer(serializers.Serializer):
        list_field = serializers.ListField(
            child=serializers.IntegerField(
                validators=[validators.MaxValueValidator(999)],
            ),
            validators=[validators.MaxLengthValidator(5)],
        )
        dict_field = serializers.DictField(
            child=serializers.IntegerField(
                validators=[validators.MaxValueValidator(999)],
            ),
        )

    @extend_schema(request=XSerializer, responses=XSerializer)
    @api_view(['POST'])
    def view_func(request, format=None):
        pass  # pragma: no cover

    schema = generate_schema('x', view_function=view_func)
    properties = schema['components']['schemas']['X']['properties']
    assert properties['list_field']['maxItems'] == 5
    assert properties['list_field']['items']['maximum'] == 999
    assert properties['dict_field']['additionalProperties']['maximum'] == 999


def test_timedelta_in_validator():
    class XSerializer(serializers.Serializer):
        field = serializers.DurationField(
            validators=[validators.MaxValueValidator(timedelta(seconds=3600))],
        )

    @extend_schema(request=XSerializer, responses=XSerializer)
    @api_view(['POST'])
    def view_func(request, format=None):
        pass  # pragma: no cover

    # `DurationField` values and `timedelta` serialize to `string` type so `maximum` is invalid.
    with pytest.raises(jsonschema.exceptions.ValidationError, match=r".* is not of type 'number'"):
        generate_schema('x', view_function=view_func)


@pytest.mark.parametrize('pattern,expected', [
    (r'\xff', r'\u00ff'),  # Unify escape characters.
    (r'\Ato\Z', r'^to$'),  # Switch to ECMA anchors.
])
def test_regex_validator_tweaks(pattern, expected):
    class XSerializer(serializers.Serializer):
        field = serializers.CharField(validators=[validators.RegexValidator(pattern)])

    @extend_schema(request=XSerializer, responses=XSerializer)
    @api_view(['POST'])
    def view_func(request, format=None):
        pass  # pragma: no cover

    schema = generate_schema('x', view_function=view_func)
    field = schema['components']['schemas']['X']['properties']['field']
    assert field['pattern'] == expected
