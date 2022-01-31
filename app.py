from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
api= Api(app)

class Publication(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))

class Publication_Schema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")

post_schema = Publication_Schema()
posts_schema = Publication_Schema(many = True)

class ResourceListBlogs(Resource):
    def get(self):
        publications = Publication.query.all()
        return posts_schema.dump(publications)

    def post(self):
        new_pub = Publication(
            title  = request.json['title'],
            content = request.json['content']
        )
        db.session.add(new_pub)
        db.session.commit()
        return post_schema.dump(new_pub)

class ResourceOnePublication(Resource):
    def get(self, id_pub):
        publication = Publication.query.get_or_404(id_pub)
        return post_schema.dump(publication)

api.add_resource(ResourceListBlogs, '/publicaciones')
api.add_resource(ResourceListBlogs, '/publicaciones')


if __name__=='__main__':
    app.run(debug = True)