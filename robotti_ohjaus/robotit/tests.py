from django.test import TestCase
from django.urls import reverse
from .models import Robotti


class RobottiListViewTests(TestCase):
	def test_homepage_shows_robot_coordinates_and_selection(self):
		Robotti.objects.create(
			modelname='Testirobotti',
			serialnumber='TEST-001',
			location_x=12.5,
			location_y=-4.25,
		)

		response = self.client.get(reverse('robotit_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Testirobotti')
		self.assertContains(response, 'TEST-001')
		self.assertContains(response, '12.5')
		self.assertContains(response, '-4.25')
		self.assertContains(response, 'robot-toggle')

	def test_homepage_shows_empty_state(self):
		response = self.client.get(reverse('robotit_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Robotteja ei ole vielä lisätty.')
