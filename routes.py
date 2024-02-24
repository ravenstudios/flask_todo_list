from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from __main__ import app
from schema import Item, db
import datetime



@app.route('/')
def index():
    return render_template('show_items.html', items=Item.query.all())



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



# @app.route('/edit-new-item', methods = ['GET', 'POST'])
# def add_new_item():
#     form_data = request.form.to_dict(flat=False)
#     item = Item(form_data)
#     db.session.add(item)
#     db.session.commit()
#     return redirect("/")


@app.route('/delete-item', methods = ['GET'])
def delete_item():
    args = request.args
    print(f"ARGGRRSSSSS:{args}")
    print(f"args:{args}")
    Item.query.filter_by(_id=args.get("_id")).delete()
    db.session.commit()
    return redirect("/")
