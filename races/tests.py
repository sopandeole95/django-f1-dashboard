# races/tests.py

import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

from .services import fetch_last_race_results
from .models import Race, Driver, Team

class FetchLastRaceResultsTests(TestCase):
    def setUp(self):
        # sample payload mimicking the Jolpi endpoint
        self.sample = {
            "MRData": {
                "RaceTable": {
                    "Races": [
                        {
                            "raceName": "Test GP",
                            "Circuit": {"circuitName": "Test Circuit"},
                            "date": "2025-06-12",
                            "Results": [
                                {
                                    "position": "1",
                                    "Driver": {"givenName": "Foo", "familyName": "Bar"},
                                    "Constructor": {"name": "Baz Racing"},
                                    "Time": {"time": "1:23.456"},
                                    "status": "Finished"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    @patch('races.services.requests.get')
    def test_fetch_success(self, mock_get):
        # mock the HTTP call
        mock_get.return_value.json.return_value = self.sample
        mock_get.return_value.raise_for_status = lambda: None

        result = fetch_last_race_results()
        self.assertEqual(result['race']['name'], "Test GP")
        self.assertEqual(result['race']['circuit'], "Test Circuit")
        self.assertEqual(result['race']['date'], "2025-06-12")

        self.assertEqual(len(result['results']), 1)
        r = result['results'][0]
        self.assertEqual(r['position'], "1")
        self.assertEqual(r['Driver']['familyName'], "Bar")

    @patch('races.services.requests.get')
    def test_fetch_empty(self, mock_get):
        mock_get.return_value.json.return_value = {"MRData": {"RaceTable": {"Races": []}}}
        mock_get.return_value.raise_for_status = lambda: None

        result = fetch_last_race_results()
        self.assertIsNone(result['race'])
        self.assertEqual(result['results'], [])


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

        # create a Team & Driver & a Race for DB-backed list view
        team = Team.objects.create(name="Alpha")
        driver = Driver.objects.create(name="Pilot", team=team)
        Race.objects.create(date="2025-06-12", name="DB GP", driver=driver, position=5)

    def test_race_list_view(self):
        resp = self.client.get(reverse('race-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "DB GP")
        self.assertContains(resp, "Pilot")

    @patch('races.views.fetch_last_race_results')
    def test_last_race_view(self, mock_fetch):
        mock_fetch.return_value = {
            "race": {"name": "Mock GP", "circuit": "Mock Circuit", "date": "2025-06-12"},
            "results": [
                {"position": "1",
                 "Driver": {"givenName": "A", "familyName": "B"},
                 "Constructor": {"name": "C"},
                 "Time": {"time": "1:23.456"},
                 "status": "Finished"}
            ]
        }
        resp = self.client.get(reverse('race-last'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Mock GP")
        self.assertContains(resp, "B, A")
