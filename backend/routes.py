from app import app, db
from flask import request,jsonify
from model import Friends

#get all friends:
@app.route("/api/friends" , methods = ["GET"])
def get_friends():
    friends = Friends.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

#create a friend:
@app.route("/api/friends" , methods = ["POST"])
def create_friend():
    try:
        data = request.json 
        required_fields = ['name' , 'role' ,'description' , 'gender']
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error" : f'Missing required field : {field}'}),400
        name = data.get('name')
        role  = data.get('role')
        description = data.get('description')
        gender = data.get('gender')
        
        if gender == "male":
            photo_url = f'https://avatar.iran.liara.run/public/boy?username={name}'
        elif gender == "female":
            photo_url = f'https://avatar.iran.liara.run/public/girl?username={name}'
        else:
            photo_url = None
            
        new_friend = Friends(name = name , role = role, description = description , gender = gender, photo_url = photo_url)
        db.session.add(new_friend)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error ": str(e)}), 500

#delete a friend:
@app.route("/api/friends/<int:id>" , methods = ["DELETE"])
def delete_friend(id):
    try:
        friend = Friends.query.get(id)
        if Friends is None:
            return jsonify({"error ": "Friend not found"}),404
        
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message": "Friend deleted Successfully"}),
    except Exception as e:
        db.session.rollback()
        return jsonify({"error ": str(e)}), 500

#update a friend:
@app.route("/api/friend/<int:id>" , methods = ['PATCH'])
def update_friend(id):
    try:
        friend = Friends.query.get(id)
        if friend is None:
            return jsonify({"error" : "Friend not found"}),404
        data = request.json
        
        friend.name = data.get("name",friend.name)
        friend.role = data.get("role",friend.role)
        friend.description = data.get("description",friend.description)
        friend.gender = data.get("gender",friend.gender)
        
        db.session.commit()
        return jsonify(friend.to_json()),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}),500