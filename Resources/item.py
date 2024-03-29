from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from Models.itemmodel import ItemModel

class Item(Resource):

  parser = reqparse.RequestParser()
  parser.add_argument(
    'price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
  )
  parser.add_argument(
    'store_id',
    type=int,
    required=True,
    help="Every item needs a store id"
  )

  @jwt_required
  def get(self, name):
    item = ItemModel.find_by_name(name)

    if item:
        return item.json()
    return {'message': 'Item not found'}, 404
  
  def post(self, name):
    if ItemModel.find_by_name(name):
      return{'message': f'An item with the name {name} already exists.'}, 400

    request_data = Item.parser.parse_args()
    item = ItemModel(name, request_data['price'], request_data['store_id'])

    try:
        item.save_to_db()
    except:
        return{'message': 'An error occurred when inserting the item'}, 500
    
    return item.json(), 201

  def delete(self, name):
    if ItemModel.find_by_name(name):
      ItemModel.delete_from_db()

      return{"message": "Item deleted"}

    return{"message":"Item not found"}, 404
    
  def put(self, name):
    request_data = Item.parser.parse_args()
    item = ItemModel.find_by_name(name)

    if Item is None:
      try:
        item = ItemModel(name, request_data['price'], request_data['store_id'])
      except:
        return{'message': 'An error occurred when inserting the item'}, 500
    else:
      try:
        item.price = request_data['price']
        item.store_id = request_data['store_id']
      except:
        return{'message': 'An occurred when updating the item'}, 500
    
    item.save_to_db()

    return item.json(), 201

class ItemList(Resource):
  def get(self):
    return{'items': [item.json() for item in ItemModel.query.all()]}
