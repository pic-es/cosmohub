import unittest

from hypothesis import given
from hypothesis import strategies
from hypothesis_sqlalchemy import tabular

from cosmohub import create_app
from cosmohub.database import model


user_strategy = tabular.records.factory(model.User.__table__, email=strategies.emails())
user_fields = ["id", "name", "email"]


def setUpModule():
    pass


def tearDownModule():
    pass


class Api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        with cls.app.app_context():
            model.db.drop_all()
            model.db.create_all()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @given(user_strategy)
    def test_user(self, user_model):
        user_data = dict(zip(user_fields[1:], user_model[1:]))

        with self.app.test_client() as client:
            # Retrieve initial empty set
            r = client.get("/api/users")
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json, [])

            # Add user
            r = client.post("/api/users", json=user_data)
            self.assertEqual(r.status_code, 201)
            added_user_data = r.json
            self.assertGreater(added_user_data.items(), user_data.items())

            # Retrieve added user
            r = client.get("/api/users/{id}".format(**added_user_data))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json, added_user_data)

            # Try to duplicate the user
            r = client.post("/api/users", json=user_data)
            self.assertEqual(r.status_code, 409)

            # Try with a malformed JSON
            r = client.post("/api/users", data="{", content_type="application/json")
            self.assertEqual(r.status_code, 400)

            # Try with an incomplete JSON
            r = client.post("/api/users", json={})
            self.assertEqual(r.status_code, 422)

            # Assert nothing was added
            r = client.get("/api/users")
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json, [added_user_data])

            # Remove user
            r = client.delete("/api/users/{id}".format(**added_user_data))
            self.assertEqual(r.status_code, 200)

            # Assert user was removed
            r = client.get("/api/users/{id}".format(**added_user_data))
            self.assertEqual(r.status_code, 404)

            # Retrieve final empty set
            r = client.get("/api/users")
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json, [])

    def test_sentry(self):
        old_value = self.app.config['PROPAGATE_EXCEPTIONS']
        try:
            self.app.config['PROPAGATE_EXCEPTIONS'] = False
            with self.app.test_client() as client:
                r = client.get("/debug-sentry")
                self.assertEqual(r.status_code, 500)

        finally:
            self.app.config['PROPAGATE_EXCEPTIONS'] = old_value


if __name__ == "__main__":
    unittest.main()
