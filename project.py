from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

# import database operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurants():
	if request.method == 'POST':
		name = request.form['name']
		if name:
			newRestaurant = Restaurant(name = request.form['name'])
			session.add(newRestaurant)
			session.commit()
			return redirect('/')
		else:
			flash("You must fill in a name.")
			return render_template('newRestaurant.html')	
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		name = request.form['name']
		if name:
			editedRestaurant.name = request.form['name']
			session.add(editedRestaurant)
			session.commit()
			return redirect('/')
		else:
			flash("You must fill in a valid name.")
			return redirect(url_for('editRestaurant', restaurant_id = restaurant_id))	
	else:
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	if request.method == 'POST':
		session.query(Restaurant).filter_by(id = restaurant_id).delete()
		session.commit()
		return redirect('/')
	else:
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	menu_items_apps = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Appetizer')
	menu_items_ent = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Entree')
	menu_items_dess = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Dessert')
	menu_items_bev = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Beverage')
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('menu.html', restaurant = restaurant, menu_items_apps = menu_items_apps, menu_items_ent = menu_items_ent, menu_items_dess = menu_items_dess, menu_items_bev = menu_items_bev)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		price = '$'+str(request.form['price'])
		course = request.form['course']
		if name and description and price and course:
			newItem = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
			session.add(newItem)
			session.commit()
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
		else:
			flash("You must fill in all fields.")
			return redirect(url_for('newMenuItem', restaurant_id = restaurant_id))	
	else:
		return render_template('newMenuItem.html', restaurant = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		price = '$'+str(request.form['price'])
		course = request.form['course']
		if name and description and price and course:
			menuItem.name = name
			menuItem.description = description
			menuItem.price = price
			menuItem.course = course
			session.add(menuItem)
			session.commit()
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
		else:
			flash("You must fill in all fields.")
			return render_template('editMenuItem.html', menu = menuItem)
	else:
		return render_template('editMenuItem.html', menu = menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	if request.method == 'POST':
		session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).delete()
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', menu = menuItem)

if __name__ == '__main__':
	app.secret_key = 'real_secret'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)