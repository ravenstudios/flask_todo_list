from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from __main__ import app
from schema import Item, db
import datetime



@app.route('/')
def index():
    return render_template('show_items.html', items=Item.query.order_by(Item.item_priority).all())



@app.route('/add-new-item-form', methods = ['GET', 'POST'])
def add_new_item_form():

    id = request.args.get('_id')
    return render_template('add_new_item_form.html', item=Item.query.get(id))


@app.route('/add-new-item', methods = ['GET', 'POST'])
def add_new_item():
    form_data = request.form.to_dict(flat=False)
    item = None
    if "_id" in form_data.keys():
        item = Item.query.get(form_data["_id"][0])

        item.item_name = form_data["item_name"][0]
        item.item_notes = form_data["item_notes"][0]
    else:
        form_data.pop('_id', None)
        item = Item(form_data)

    db.session.add(item)
    db.session.commit()
    return redirect("/")


@app.route('/delete-item', methods = ['GET'])
def delete_item():
    args = request.args
    Item.query.filter_by(_id=args.get("_id")).delete()
    db.session.commit()
    return redirect("/")


@app.route('/toggle-completed', methods = ['GET'])
def toggle_completed():
    id = request.args.get('_id')
    item=Item.query.get(id)
    checked = request.args.get('checked')

    if checked == "true":
        item.item_completed = True
    else:
        item.item_completed = False
    db.session.commit()
    return redirect("/")



@app.route('/change-item-priority-up', methods = ['GET'])
def change_item_priority_up():
    item_id = request.args.get('_id', type=int)

    item_to_move = Item.query.get(item_id)
    item_to_swap = Item.query.get(item_id - 1)
    if item_to_move and item_to_swap:
        item_to_move.item_priority, item_to_swap.item_priority = item_to_swap.item_priority, item_to_move.item_priority
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/change-item-priority-down', methods = ['GET'])
def change_item_priority_down():
    item_id = request.args.get('_id', type=int)

    item_to_move = Item.query.get(item_id)
    item_to_swap = Item.query.get(item_id + 1)
    if item_to_move and item_to_swap:
        item_to_move.item_priority, item_to_swap.item_priority = item_to_swap.item_priority, item_to_move.item_priority
        db.session.commit()
    return redirect(url_for('index'))
