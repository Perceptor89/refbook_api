from django.test import TestCase
from refbook.models import Refbook, RefbookElement, RefbookVersion
from django.urls import reverse
from refbook import utils
from datetime import date
import unittest
from freezegun import freeze_time
from django.db.utils import IntegrityError


class TestRefbookListView(TestCase):
    fixtures = ['data']

    def test_refbook_list(self):
        response = self.client.get(reverse('refbook-list')).json()
        names = [r['name'] for r in response['refbooks']]
        self.assertEqual(['Первый справочник', 'Второй справочник'], names)

    def test_refbook_date_has_inactual(self):
        response = self.client.get(
            reverse('refbook-list'), data={'date': '2023-08-15'}
        ).json()
        names = [r['name'] for r in response['refbooks']]
        self.assertEqual(['Первый справочник'], names)

    def test_refbook_date_all_actual(self):
        response = self.client.get(
            reverse('refbook-list'), data={'date': '2023-08-24'}
        ).json()
        names = [r['name'] for r in response['refbooks']]
        self.assertEqual(['Первый справочник', 'Второй справочник'], names)

    def test_refbook_date_no_actual(self):
        response = self.client.get(
            reverse('refbook-list'), data={'date': '2023-07-01'}
        ).json()
        names = [r['name'] for r in response['refbooks']]
        self.assertEqual([], names)

    def test_refbook_date_not_valid(self):
        response = self.client.get(
            reverse('refbook-list'), data={'date': '2023-0701'}
        )
        self.assertEqual(response.status_code, 400)


class TestConstraints(TestCase):
    fixtures = ['data']

    def test_refbook_code_constraint(self):
        refbook = Refbook.objects.get(id=1)
        self.assertEqual(refbook.code, 'Ф123')
        self.assertRaises(
            IntegrityError,
            Refbook.objects.create,
            code='Ф123',
            name='Первый справочник',
        )

    def test_refbook_version_constraint(self):
        version = RefbookVersion.objects.get(id=1)
        self.assertEqual([version.refbook.id, version.version], [1, '90'])
        self.assertRaises(
            IntegrityError,
            RefbookVersion.objects.create,
            refbook=version.refbook,
            version=version.version,
            active_from='0001-01-01',
        )

    def test_refbook_active_from_constraint(self):
        version = RefbookVersion.objects.get(id=1)
        self.assertEqual(str(version.active_from), '2023-08-01')
        self.assertRaises(
            RefbookVersion.DoesNotExist,
            RefbookVersion.objects.get,
            version='99',
        )
        self.assertRaises(
            IntegrityError,
            RefbookVersion.objects.create,
            refbook=version.refbook,
            version='99',
            active_from=version.active_from,
        )

    def test_version_code_constraint(self):
        element = RefbookElement.objects.get(id=1)
        self.assertEqual(element.code, 'k35')
        self.assertRaises(
            IntegrityError,
            RefbookElement.objects.create,
            refbook_version=element.refbook_version,
            code=element.code,
        )


class TestRefbookElementListView(TestCase):
    fixtures = ['data']

    @freeze_time('2023-08-15')
    def test_no_query_cur_version_exist(self):
        refbook = Refbook.objects.get(id=1)
        self.assertEqual(len(refbook.versions.all()), 4)

        cur_ver = refbook.current_version()
        self.assertEqual(str(cur_ver.active_from),
                         '2023-08-15')
        self.assertEqual(cur_ver.version, '110')
        self.assertEqual(len(cur_ver.elements.all()), 3)

        elements = RefbookElement.objects\
            .filter(refbook_version__refbook=1)
        self.assertEqual(len(elements), 7)

        response = self.client.get(
            reverse('refbook-element-list', kwargs={'pk': 1}),
        ).json()
        codes = [e['code'] for e in response['elements']]
        self.assertEqual(['k35', 'G58', 'O67'], codes)

    @freeze_time('2023-08-15')
    def test_no_query_cur_version_not_exist(self):
        refbook = Refbook.objects.get(id=2)
        self.assertEqual(len(refbook.versions.all()), 1)

        cur_ver = refbook.current_version()
        self.assertIsNone(cur_ver)

        response = self.client.get(
            reverse('refbook-element-list', kwargs={'pk': 2}),
        ).json()
        codes = [e['code'] for e in response['elements']]
        self.assertEqual(codes, [])

    @freeze_time('2023-08-15')
    def test_is_query_not_cur_ver(self):
        response = self.client.get(
            reverse('refbook-element-list', kwargs={'pk': 1}),
            data={'version': 100},
        ).json()
        codes = [e['code'] for e in response['elements']]
        self.assertEqual(['111', '222'], codes)


class TestRefbookElementCheckView(TestCase):
    fixtures = ['data']

    def test_no_required_field(self):
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': 111},
        )
        self.assertEqual(response.status_code, 400)

    @freeze_time('2023-08-15')
    def test_cur_version_is_element(self):
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': 'k35', 'value': 'первый элемент'},
        )
        self.assertEqual(response.status_code, 200)

    @freeze_time('2023-08-15')
    def test_cur_version_no_element(self):
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': 'k35', 'value': 'второй элемент'},
        )
        self.assertEqual(response.status_code, 404)

    @freeze_time('2023-08-15')
    def test_not_cur_version_is_element(self):
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': '333', 'value': 'третий', 'version': 90},
        )
        self.assertEqual(response.status_code, 200)

    @freeze_time('2023-08-15')
    def test_not_cur_version_no_element(self):
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': '333', 'value': 'нет такого', 'version': 90},
        )
        self.assertEqual(response.status_code, 404)

    @freeze_time('2023-08-15')
    def test_version_not_exist(self):
        self.assertFalse(RefbookVersion.objects.filter(version='99').exists())
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': '333', 'value': 'нет такого', 'version': 99},
        )
        self.assertEqual(response.status_code, 404)

    @freeze_time('2023-08-15')
    def test_other_refbook_element(self):
        self.assertTrue(
            RefbookElement.objects.filter(
                refbook_version__refbook=2,
                refbook_version__version='100',
                code='25ЕР',
                value='пятый',
            ).exists()
        )
        response = self.client.get(
            reverse('refbook-check-element', kwargs={'pk': 1}),
            data={'code': '25ЕР', 'value': 'пятый', 'version': 100},
        )
        self.assertEqual(response.status_code, 404)


class TestUtils(unittest.TestCase):
    def test_convert_date(self):
        self.assertIs(utils.convert_date(25), None)
        self.assertIs(utils.convert_date('25'), None)
        self.assertIs(type(utils.convert_date('2025-10-29')), date)
