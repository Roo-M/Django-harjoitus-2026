from django.test import TestCase
from django.urls import reverse
from .models import Location, Robotti
from .serializers import RobottiSerializer


class RobottiListViewTests(TestCase):
	def test_homepage_shows_robot_locations_and_selection(self):
		robotti = Robotti.objects.create(modelname='Testirobotti', serialnumber='TEST-001')
		Location.objects.create(robotti=robotti, location_x=12.5, location_y=-4.25)
		Location.objects.create(robotti=robotti, location_x=8.0, location_y=3.5)
		Robotti.objects.create(modelname='Toinen robotti', serialnumber='TEST-002')

		response = self.client.get(reverse('robotit_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Testirobotti')
		self.assertContains(response, 'TEST-001')
		self.assertContains(response, '12.5')
		self.assertContains(response, '-4.25')
		self.assertContains(response, '8.0')
		self.assertContains(response, '3.5')
		self.assertContains(response, 'robot-toggle')
		table_rows = response.content.decode().split('<tbody id="coordinate-rows">')[1].split('</tbody>')[0]
		self.assertEqual(table_rows.count('Testirobotti'), 1)
		self.assertEqual(table_rows.count('TEST-001'), 1)
		self.assertEqual(table_rows.count('class="robot-separator"'), 1)

	def test_homepage_shows_empty_state(self):
		response = self.client.get(reverse('robotit_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Robotteja ei ole vielä lisätty.')


class RobottiSerializerTests(TestCase):
	def test_duplicate_robot_adds_location_without_creating_robot(self):
		first = RobottiSerializer(data={
			'modelname': 'Testirobotti',
			'serialnumber': 'TEST-001',
			'location_x': 12.5,
			'location_y': -4.25,
		})
		self.assertTrue(first.is_valid(), first.errors)
		original_robot = first.save()

		second = RobottiSerializer(data={
			'modelname': 'Testirobotti',
			'serialnumber': 'TEST-001',
			'location_x': 8.0,
			'location_y': 3.5,
		})
		self.assertTrue(second.is_valid(), second.errors)
		duplicate_robot = second.save()

		self.assertEqual(Robotti.objects.count(), 1)
		self.assertEqual(original_robot.pk, duplicate_robot.pk)
		self.assertEqual(duplicate_robot.locations.count(), 2)
