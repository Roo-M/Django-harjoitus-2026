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

	def test_consecutive_zero_coordinates_are_not_added(self):
		first = RobottiSerializer(data={
			'modelname': 'Testirobotti',
			'serialnumber': 'TEST-ZERO',
			'location_x': 0,
			'location_y': 0,
		})
		self.assertTrue(first.is_valid(), first.errors)
		robot = first.save()

		second = RobottiSerializer(data={
			'modelname': 'Testirobotti',
			'serialnumber': 'TEST-ZERO',
			'location_x': 0,
			'location_y': 0,
		})
		self.assertTrue(second.is_valid(), second.errors)
		second.save()

		self.assertEqual(robot.locations.count(), 1)

	def test_zero_coordinates_after_a_nonzero_location_are_added(self):
		robot = Robotti.objects.create(modelname='Testirobotti', serialnumber='TEST-ZERO-2')
		Location.objects.create(robotti=robot, location_x=1, location_y=2)

		serializer = RobottiSerializer(robot, data={
			'modelname': 'Testirobotti',
			'serialnumber': 'TEST-ZERO-2',
			'location_x': 0,
			'location_y': 0,
		})
		self.assertTrue(serializer.is_valid(), serializer.errors)
		serializer.save()

		self.assertEqual(robot.locations.count(), 2)
