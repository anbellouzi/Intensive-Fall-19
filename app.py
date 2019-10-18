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
reservation = db.reservation
comments = db.comments

app = Flask(__name__)

@app.route('/')
def parking_index():
    """Show all parking."""
    all_parkings = parkings.find()
    print(all_parkings)
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
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'address': request.form.get('address'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'img': request.form.get('images'),
        'start_date': request.form.get('start_date'),
        'start_time': request.form.get('start_time'),
        'start_min': request.form.get('start_min'),
        'start_ampm': request.form.get('start_ampm'),
        'end_date': request.form.get('end_date'),
        'end_time': request.form.get('end_time'),
        'end_min': request.form.get('end_min'),
        'end_ampm': request.form.get('end_ampm'),
    }
    parking_id = parkings.insert_one(parking).inserted_id
    return redirect(url_for('show_parking', parking_id=parking_id))

@app.route('/parking/<parking_id>')
def show_parking(parking_id):
    """Show a single parking."""
    parking = parkings.find_one({'_id': ObjectId(parking_id)})
    parking_comments = comments.find({'parking_id': ObjectId(parking_id)})
    return render_template('parking_show.html', parking=parking, comments=parking_comments)

@app.route('/parking/<parking_id>/edit', methods=['POST', 'GET'])
def items_edit(parking_id):
    """Show the edit form for a item."""
    parking = parkings.find_one({'_id': ObjectId(parking_id)})
    return render_template('parking_edit.html', parking=parking, title='Edit Parking')

@app.route('/parking/<parking_id>', methods=['POST'])
def items_update(parking_id):
    """Submit an edited item."""
    updated_parking = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'address': request.form.get('address'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'img': request.form.get('images'),
        'start_date': request.form.get('start_date'),
        'start_hour': request.form.get('start_hour'),
        'start_min': request.form.get('start_min'),
        'start_ampm': request.form.get('start_ampm'),
        'end_date': request.form.get('end_date'),
        'end_hour': request.form.get('end_hour'),
        'end_min': request.form.get('end_min'),
        'end_ampm': request.form.get('end_ampm'),
    }
    parkings.update_one(
        {'_id': ObjectId(parking_id)},
        {'$set': updated_parking})
    return redirect(url_for('show_parking', parking_id=parking_id))


@app.route('/parking/<parking_id>/delete', methods=['POST'])
def item_delete(parking_id):
    """Delete one parking."""
    parkings.delete_one({'_id': ObjectId(parking_id)})
    return redirect(url_for('parking_index'))

@app.route('/book/parking/<parking_id>', methods=['POST'])
def add_shopping_cart(parking_id):
    """Show a single playlist."""
    parking = parkings.find_one({'_id': ObjectId(parking_id)})
    book.parking = parking
    book.save(parking)
    book_parking = book.find()
    return render_template('book.html', book_parking=parking)


@app.route('/confirmation', methods=['POST'])
def reservation_submit():
    """Submit a new parking."""
    start_date = request.form.get('start_date')
    start_hour = request.form.get('start_hour')
    start_min = request.form.get('start_min')
    start_ampm = request.form.get('start_ampm')
    start_time = str(start_hour)+':'+str(start_min)+' '+str(start_ampm)+' '+str(start_date)

    end_date = request.form.get('end_date')
    end_hour = request.form.get('end_hour')
    end_min = request.form.get('end_min')
    end_ampm = request.form.get('end_ampm')
    end_time = str(end_hour)+':'+str(end_min)+' '+str(end_ampm)+' '+str(end_date)

    reserve = {
        'name': request.form.get('name'),
        'car': request.form.get('car'),
        'car_plates': request.form.get('car_plates'),
        'car_color': request.form.get('car_color'),
        'car_type': request.form.get('car_type'),
        'referral': request.form.get('referral'),
        'address': request.form.get('address'),
        'start_time': start_time,
        'end_time': end_time,
        'parking_id': ObjectId(request.form.get('parking_id'))

    }
    reservation_id = reservation.insert_one(reserve).inserted_id
    return redirect(url_for('show_confirmation', reservation_id=reservation_id))


@app.route('/confirmation/<reservation_id>')
def show_confirmation(reservation_id):
    """Submit a new parking."""
    reserve = reservation.find_one({'_id': ObjectId(reservation_id)})
    return render_template('confirmation.html', reservation=reserve)

@app.route('/search', methods=['GET', 'POST'])
def search_parking():
    """Submit a new parking."""

    phrase = request.args.get('search_term')

    query_term = { "address": { "$regex": phrase.title() } }

    results = parkings.find(query_term)

    return render_template('parkings.html', parkings=results, title=phrase)



@app.route('/parking/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'created_at': datetime.now(),
        'parking_id': ObjectId(request.form.get('parking_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id

    return redirect(url_for('show_parking', parking_id=request.form.get('parking_id')))

@app.route('/parking/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('show_parking', parking_id=comment.get('parking_id')))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
