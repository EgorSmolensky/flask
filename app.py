from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from errors import HttpException
from schema import validate, CreateUserSchema
import datetime


app = Flask(__name__)

POSTGRES_USER = ''
POSTGRES_PASSWORD = ''

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/netology_flask'
db = SQLAlchemy(app)

@app.errorhandler(HttpException)
def error_handler(error: HttpException):
    http_response = jsonify({
        'status': 'error',
        'message': error.message,
    })
    http_response.status_code = error.status_code
    return http_response


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Пользователь {self.id}>'


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Объявление {self.id}: {self.title}. Владелец: {self.owner_id}>'


with app.app_context():
    db.drop_all()
    db.create_all()


def get_ann(ann):
    return {
        "id": ann.id,
        "title": ann.title,
        "description": ann.description,
        "created_at": ann.created_at,
        "owner_id": ann.owner_id
    }


@app.route("/register/", methods=["POST", ])
def register():
    user_data = validate(request.json, CreateUserSchema)
    try:
        hash = generate_password_hash(user_data['password'])
        u = User(email=user_data['email'], password=hash)
        db.session.add(u)
        db.session.commit()
    except Exception as e:
        raise HttpException(400, 'Registration failed. ' + str(e))
    return jsonify({'status': 'register_success', 'user_id': u.id})


@app.route("/ads/", methods=["GET"])
def get_advts():
    anns = [get_ann(ann) for ann in Announcement.query.all()]
    return jsonify({"announcements": anns})


@app.route("/ads/", methods=["POST"])
def create_advt():
    data = request.json
    ann = Announcement(**data)
    db.session.add(ann)
    db.session.commit()
    return jsonify({'ann_id': ann.id, 'status': 'created'})


@app.route("/ads/<int:ad_id>/", methods=["GET", ])
def get_advt(ad_id):
    try:
        ad = Announcement.query.filter_by(id=ad_id).first()
        return jsonify(get_ann(ad))
    except Exception as e:
        raise HttpException(404, 'Объявление не найдено')


@app.route("/ads/<int:ad_id>/", methods=["DELETE", ])
def delete_advt(ad_id):
    try:
        ad = Announcement.query.filter_by(id=ad_id).first()
        db.session.delete(ad)
        db.session.commit()
        return jsonify({'status': 'deleted'})
    except Exception as e:
        raise HttpException(404, 'Объявление не найдено')


@app.route("/ads/<int:ad_id>/", methods=["PATCH", ])
def patch_advt(ad_id):
    try:
        data = request.json
        ad = Announcement.query.filter_by(id=ad_id).first()
        ad.title = data.get('title', ad.title)
        ad.description = data.get('description', ad.description)
        db.session.add(ad)
        db.session.commit()
        return jsonify({'ann_id': ad.id, 'status': 'patched'})
    except Exception as e:
        raise HttpException(404, 'Объявление не найдено')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)
