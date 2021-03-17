import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMGFmZmIzN2QwMDA2ODI2MTQxYiIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQ0OTgwOTEsImV4cCI6MTYxNDU4NDQ5MSwiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Mod3ZQYs20h8i49VCLCW0D5GFDAHR6hHkgbx0MynMLu35v_FuMYtdMftPQirAlm6jEjzv9LQyJNqSsL3rV6MRtCHgJG0-zxslKpA4c_zxMzbMEmBJFWJaTokwxf4OXH3DZUmZcWIwbSy97rF5CGbMk5Bv0t87Ine8Xklyu6o8ZklCUEkgwTb9rMnzUzGJm7KqznOBo8CUK0TEiOzsqfi5tqgI-KcnRjJYRvuoshVOvJeanMcOXlpjd9ebOO6QjJOR7nlLLqE6J_NIDTLYEu2iKwfcMyDrClhMoikGw-AY1rxdQ0_z6aueZmywyDJo6L7r15TYyrNVQqLN4EtiTIXLQ'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMDgyZjdiMTUxMDA3MDM4NDM5MSIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQ0OTgzMjMsImV4cCI6MTYxNDU4NDcyMywiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.bM00n13NvPxrJdqsqlZDP5WvwRaIv7UIGm-x6FHdo2k9qi79Y5rXko-tMG7UyjxIzhT_L4oSbz2k2UBh79eaRRF6jYbmNyYVaV8w24KLHU_4caZDdxfgHEWHDs-KWJfxCFmJcz6o3vgqTWktz8dn0Wa0vu8i4zX1UQ6f-izoTKTrqP7A-YWgFuPOk7t97UuPt8sDFMcnJfgYDAVZeokWfcbkamEgVPMcSYkGjcVLBsqxEk2SaZnKk0cc-GSQ-A8Xd8VIoRgdsoiS3Eh25PSL_UIlLQ0AvvHk0BoEMqZIk_OK-47497EznYmyRlr9HHjfqGJYcjcnCjvfk6iveUAEWA'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMDQxZmIzN2QwMDA2ODI2MTNmZCIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQ0OTg0MjMsImV4cCI6MTYxNDU4NDgyMywiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.SNwwLN7TyOcgVki7cAqXw89C46nIVb2NReA09LKb0hLrqx3MsriBhgqi96eXI96e8YslLDEK7f8WZiOBkGxG2DFTi2mpwuAOiMLrDPGKJTdyii3PojEfCkrF7J1MXxlUIlbk70Zw5Nbxtw5mKAAuc5KHxvHz94gsml0RsGzVFsF1v1yPLaFf8XWhR4nns_2hzlOV8t79OFC-1sWAct0bgtmg_hVWNoaNLbNUXaGwpzgONRYcV0N0xMM6fPLDzrEAjaElw-9N7k7bY6BbYO_PDisx5-BYRZsXNRttsQtHPK-vqUAETChAkdtYW5YMjLRa2RqfsU-lYv6hkC2QTqCvZw'


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URL')
        setup_db(self.app)

    def tearDown(self):
        pass

    def test_add_actors(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Ryan Reynolds', 'age': '35', 'gender': 'male'},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['actor'])

    def test_bad_request_in_add_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', 'gender': ''},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(
            data['message'],
            'Bad Request, please check your inputs'
        )
        self.assertEqual(data['success'], False)

    def test_edit_actors(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Jack Black'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['actor'])

    def test_not_found_in_edit_actor(self):
        response = self.client().patch(
            '/actors/1000',
            json={'name': 'K'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_add_movies(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Schitts Creek', 'release_date': '2020/02/01'},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['movie'])

    def test_bad_request_in_add_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ''},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(
            data['message'],
            'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)

    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'Jumanji'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['movie'])

    def test_not_found_in_edit_movie(self):
        response = self.client().patch(
            '/movies/1000',
            json={'title': 'J'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_bad_request_in_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': ''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(
            data['message'],
            'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delete'], '1')
        self.assertTrue(data['success'])

    def test_not_found_delete_movie(self):
        response = self.client().delete(
            '/movies/1005',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
            )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_unauthorised_add_actors(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Kafilat', 'age': '23', 'gender': 'female'},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_unauthorised_in_edit_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'K'},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_unauthorised_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
