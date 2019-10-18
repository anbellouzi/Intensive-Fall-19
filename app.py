from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Parking')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
parkings = db.parkings
cars = db.cars
book = db.book
comments = db.comments

app = Flask(__name__)

@app.route('/')
def parking_index():
    """Show all parking."""
    all_parkings = parkings.find()
    return render_template('index.html', parkings=all_parkings)

@app.route('/parkings/')
def parkings_show_all():
    """Show all parkings."""
    all_parkings = parkings.find()
    return render_template('parkings.html', parkings=all_parkings)

@app.route('/parking/new')
def parking_new():
    """Create a new parking."""
    return render_template('parking_new.html', parking={}, title='New Parking')

@app.route('/parkings', methods=['POST'])
def parking_submit():
    """Submit a new parking."""
    parking = {
        'address': request.form.get('address'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'img': request.form.get('images'),
        # 'date': datetime.now().strftime('%A, %d %B, %Y'),
        # 'time': datetime.now().strftime('%I:%M %p')
    }
    parking_id = parkings.insert_one(parking).inserted_id
    return redirect(url_for('show_parking', parking_id=parking_id))
#
# @app.route('/parking/<parking_id>')
# def show_parking(parking_id):
#     """Show a single parking."""
#     parking = parkings.find_one({'_id': ObjectId(parking_id)})
#     parking_comments = comments.find({'parking_id': ObjectId(parking_id)})
#     return render_template('parking_show.html', parking=parking, comments=parking_comments)
#
# @app.route('/parking/<parking_id>/edit', methods=['POST', 'GET'])
# def items_edit(parking_id):
#     """Show the edit form for a item."""
#     parking = parkings.find_one({'_id': ObjectId(parking_id)})
#     return render_template('parking_edit.html', parking=parking, title='Edit Parking')
#
# @app.route('/parking/<parking_id>', methods=['POST'])
# def items_update(parking_id):
#     """Submit an edited item."""
#     updated_parking = {
#         'address': request.form.get('address'),
#         'description': request.form.get('description'),
#         'price': request.form.get('price'),
#         'img': request.form.get('images'),
#     }
#     parkings.update_one(
#         {'_id': ObjectId(parking_id)},
#         {'$set': updated_parking})
#     return redirect(url_for('show_parking', parking_id=parking_id))
#
#
# @app.route('/parking/<parking_id>/delete', methods=['POST'])
# def item_delete(parking_id):
#     """Delete one parking."""
#     parkings.delete_one({'_id': ObjectId(parking_id)})
#     return redirect(url_for('parking_index'))
#
# @app.route('/book/parking/<parking_id>', methods=['POST'])
# def add_shopping_cart(parking_id):
#     """Show a single playlist."""
#     parking = parkings.find_one({'_id': ObjectId(parking_id)})
#     book.parking = parking
#     book.save(parking)
#     book_parking = book.find()
#     return render_template('book.html', book_parking=parking)

#
# @app.route('/shopping_cart/<item_id>')
# def show_shopping_cart(item_id):
#     """Show a single playlist."""
#     cart_items = cart.find()
#     total = 0
#     for item in cart_items:
#         total += int(float(item['price']))
#
#     cart_items = cart.find()
#     return render_template('shopping_cart.html', cart_items=cart_items, total=total)
#

# @app.route('/cart/<cart_id>/delete', methods=['POST'])
# def cart_delete(cart_id):
#     """Delete one item."""
#     cart.delete_one({'_id': ObjectId(cart_id)})
#
#     return redirect(url_for('show_shopping_cart', item_id=cart_id))
#
#
# @app.route('/item/comments', methods=['POST'])
# def comments_new():
#     """Submit a new comment."""
#     comment = {
#         'title': request.form.get('title'),
#         'content': request.form.get('content'),
#         'created_at': datetime.now(),
#         'item_id': ObjectId(request.form.get('item_id'))
#     }
#     comment_id = comments.insert_one(comment).inserted_id
#
#     return redirect(url_for('show_parking', item_id=request.form.get('item_id')))
#
# @app.route('/item/comments/<comment_id>', methods=['POST'])
# def comments_delete(comment_id):
#     """Action to delete a comment."""
#     comment = comments.find_one({'_id': ObjectId(comment_id)})
#     comments.delete_one({'_id': ObjectId(comment_id)})
#     return redirect(url_for('show_parking', item_id=comment.get('item_id')))
#



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
