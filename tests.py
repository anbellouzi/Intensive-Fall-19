from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app
from datetime import datetime

sample_parking_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_parking = {
    'address': '1234 California st. San Francisco, CA 94121',
    'description': 'Cross section California st and Powell st. Parking is behind water hydrent.',
    'price': '5',
    'img': 'images',
}

sample_form_data = {
    'address': sample_parking['address'],
    'description': sample_parking['description'],
    'img': sample_parking['img'],
    'price': sample_parking['price'],

}

class ParkingTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the Parking homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Park', result.data)

    def test_new(self):
        """Test the new parking creation page."""
        result = self.client.get('/parking/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Parking', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_item(self, mock_find):
        """Test showing a single parking."""
        mock_find.return_value = sample_parking
        result = self.client.get(f'/parking/{sample_parking_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'1234 California st. San Francisco, CA 94121', result.data)
    #
    # @mock.patch('pymongo.collection.Collection.find_one')
    # def test_edit_item(self, mock_find):
    #     """Test editing a single item."""
    #     mock_find.return_value = sample_item
    #
    #     result = self.client.get(f'/items/{sample_item_id}/edit')
    #     self.assertEqual(result.status, '200 OK')
    #     self.assertIn(b'Peperica', result.data)
    #
    # @mock.patch('pymongo.collection.Collection.update_one')
    # def test_update_playlist(self, mock_update):
    #     result = self.client.post(f'/item/{sample_item_id}', data=sample_form_data)
    #
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_update.assert_called_with({'_id': sample_item_id}, {'$set': sample_item})
    #
    # @mock.patch('pymongo.collection.Collection.delete_one')
    # def test_delete_item(self, mock_delete):
    #     form_data = {'_method': 'DELETE'}
    #     result = self.client.post(f'/items/{sample_item_id}/delete', data=form_data)
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_delete.assert_called_with({'_id': sample_item_id})

if __name__ == '__main__':
    unittest_main()
