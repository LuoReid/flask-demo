
import unittest
from unittest import result

from app import app, db, Movie, User, forge, initdb


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        db.create_all()
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year=2022)
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        res = self.client.get('/nothing')
        data = res.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(res.status_code, 404)

    def test_index_page(self):
        res = self.client.get('/')
        data = res.get_data(as_text=True)
        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(res.status_code, 200)

    def login(self):
        self.client.post('/login', data=dict(username='test',
                         password='123'), follow_redirects=True)

    def logout(self):
        self.client.post('/logout', follow_redirects=True)

    def test_create_item(self):
        self.login()
        res = self.client.post(
            '/', data=dict(title='New Movie', year=2022), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Item created.', data)
        self.assertIn('New Movie', data)

        res = self.client.post(
            '/', data=dict(title='', year=2022), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

        res = self.client.post(
            '/', data=dict(title='New Movie', year=''), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

    def test_update_item(self):
        self.login()

        res = self.client.get('/movies/1/edit')
        data = res.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2022', data)

        res = self.client.post(
            '/movies/1/edit', data=dict(title='New Movie Edited', year=2023), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Item updated.', data)
        self.assertIn('New Movie Edited', data)

        res = self.client.post(
            '/movies/1/edit', data=dict(title='', year=2023), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Item upated.', data)
        self.assertIn('Invalid input.', data)

        res = self.client.post(
            '/movies/1/edit', data=dict(title='New Movie Edited Again', year=''), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertNotIn('New Movie Edited Again', data)
        self.assertIn('Invalid input.', data)

    def test_delete_item(self):
        self.login()

        res = self.client.post('/movies/1/delete', follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)

    def test_login_protect(self):
        res = self.client.get('/')
        data = res.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    def test_login(self):
        res = self.client.post(
            '/login', data=dict(username='test', password='123'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Login success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

        # self.logout()
        res = self.client.post(
            '/login', data=dict(username='test', password='456'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        res = self.client.post(
            '/login', data=dict(username='wrong', password='123'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        res = self.client.post(
            '/login', data=dict(username='', password='123'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

        res = self.client.post(
            '/login', data=dict(username='test', password=''), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

    def test_logout(self):
        self.login()

        res = self.client.get('/logout', follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

    def test_settings(self):
        self.login()

        res = self.client.get('/settings')
        data = res.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        res = self.client.post(
            '/settings', data=dict(name='Grey Li'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Settings updated.', data)
        self.assertIn('Grey Li', data)

        res = self.client.post(
            '/settings', data=dict(name=''), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('Settings updated.', data)
        self.assertIn('Invalid input.', data)

    def test_forge_command(self):
        res = self.runner.invoke(forge)
        self.assertIn('Done.', res.output)
        self.assertNotEqual(Movie.query.count(), 0)

    def test_initdb_command(self):
        res = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', res.output)

    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        res = self.runner.invoke(
            args=['admin', '--username', 'grey', '--password', '123'])
        self.assertIn('Creating user ...', res.output)
        self.assertIn('Done.', res.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'grey')
        self.assertTrue(User.query.first().validate_password('123'))

    def test_admin_command_update(self):
        res = self.runner.invoke(
            args=['admin', '--username', 'peter', '--password', '456'])
        self.assertIn('Updating user ...', res.output)
        self.assertIn('Done.', res.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(User.query.first().validate_password('456'))


if __name__ == '__main__':
    unittest.main()
