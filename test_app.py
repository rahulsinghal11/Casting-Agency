import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMGFmZmIzN2QwMDA2ODI2MTQxYiIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQzNDQ2NjYsImV4cCI6MTYxNDQzMTA2NiwiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.kecKQG8TR_ZJj0WVABLRixwNewSJJDtVr96oIAnpwhN6iQ7hvtx6tgPW5eyMnu97VF-wCpNBf9-BKY-52YCC1VKGLQ3I1Fi996MhGWElIeH4PX3ZE98eTqnT2Q-Md-hC9V4by6OvKc88WJHyJ40kjDFV0ktDnoaskekmgPH_wk_8K3mdSsn5Bl5-u8DXFTV1ikrpdNCKgGnUZ9G_inQ3AP2NQ6GWalXYBvNyprz-RG3ZKAWskJ3UqPT5WRHcMdyGdnpKFbEZWrTYLQasgNVTCoVHBdWt5Ikb-DnzKVkz8aQa6wqwv7iuAO8EB0ihDRtxUXxURMDlGwJ7sSZ-yACF3A'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMDgyZjdiMTUxMDA3MDM4NDM5MSIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQzNDUzMjAsImV4cCI6MTYxNDQzMTcyMCwiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.bfE9vueRAnuPTm-grcgwOZsfMK3YUPEY9MhbYZ4FDsAQhbWiUnBUIn5viYzUSXla0k2PYp9FZk6RPeSIrt754KXquZxIcAzBSkrIbovmOqVvCS9FZ_KgeqgknGCaFOdhptkWpLspN8EZnLGVdsq4FEpbm5nIbMco4NYZ2AdTTZwa3ZUDKvhaDEvQ6hz5tqxxBIP7XAUYLYzBSrm-3EXTM5Ys1St7RwAJbD-hmeHFZk9haX9vQp7p-bykuYXPpG-h2cyTNZdRpRO6sTQoHK7T37Ti4KLxCtGpXw41SZW9RQV5W98CKVZFrgrYTTJY0lPmOxLs0eNLXouTbFXTrObe3g'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhLNTZLR0NKcjJSdzV6S3NIR3h6ayJ9.eyJpc3MiOiJodHRwczovL2NvZGVicm8udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzdiMDQxZmIzN2QwMDA2ODI2MTNmZCIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMC8iLCJpYXQiOjE2MTQzNDUyNjQsImV4cCI6MTYxNDQzMTY2NCwiYXpwIjoiYXkzSkNUcmZVTkFhUFFza1djcFlORExFQVVNQ2NVcUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.da8skwRZHuIdKJLJ4i2ibAwAKs89LxpbxNgahj-1AnA3gCX9F6QDsrqCfgOxNwK-ccHSxf6XmERiiT-dc2syE2J4j3SmngHyZaf_gSIe2r2KcxIWNMLHYdZI56tWWDLLCNYNcWsHx6sbSHyw2-LpZnJwn7KUn7sLrNSkUpLPI7OXc5zu1CB9rMQNEywVGxP7_nRpQyU2EevKl9EGy61TIHzwwzsTD9F7FOsn_7mZQU7Bq51e1jR5NKoIal4a_gjH-a3PuvpEdD4X4pS0UQvi_A3IRJH4a0NJKAQ_RXgA8tUo4sucxaibyaBzD8c5w02K9BmN66Ds7G8yQbJlW97cUg'


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
            json={'name': 'Kafee'},
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

    def test_bad_request_in_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': ''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(
            data['message'],
            'Bad Request, please check inputs'
        )
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
