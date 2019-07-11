import re
import datetime
import string
import pytz

from sqlalchemy import or_, and_, text

from sqlalchemy.ext.hybrid import hybrid_property

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime

from blogexample.app import db


# https://stackoverflow.com/questions/25668092/flask-sqlalchemy-many-to-many-insert-data
post_tags_table = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),    ##ORDER IS IMPORTANT!!! 
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))       ##PARENT FIRST, CHILD NEXT
    )


class Post(ResourceMixin, db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
   # short_description = db.Column(db.String())
    body = db.Column(db.String(), nullable=False)
    # time = DateTimeField(default=datetime.now)
    url = db.Column(db.String(128), nullable=False, unique=True)
    visible = db.Column(db.Boolean(), index=True, nullable=False, server_default='1')

    # tags_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tags = db.relationship('Tag', secondary=post_tags_table)#, backref=db.backref('post_tags_table', lazy='dynamic'))
    #tags = db.relationship('Tag', secondary=wiki_tags_table, backref=db.backref('wiki_tags_table', lazy='dynamic'))
    #@staticmethod
    @classmethod
    def create_url(cls, line):
        line = re.sub(r"[^\w\s]", "", line).strip()
        line = line[:64].strip()
        line = line.replace(" ","_").lower()
        return line

    # def addTag(self,tag):
    #     tag = tag.strip().replace(" ","_").lower()
    #     try:
    #         db_tag = Tag.get(Tag.tag==tag)
    #     except Tag.DoesNotExist:    
    #         db_tag = Tag(tag=tag)
    #         db_tag.save()

        # db_post_to_tag = Post_To_Tag(tag = db_tag,post = self)
        # db_post_to_tag.save()

    @classmethod
    def create_blogpost(cls, params):
        """
        Return whether or not the blogpost was created successfully.
        params are in admin/views/coupons_new
        params = {
            'title': coupon.code,
            'body': coupon.duration,
        }
        :return: bool
        """
        blog_params = params
        blog_params['url'] = Post.create_url(params['title'])

        print('CREATING BLOG POST NOW with params', blog_params)
        post = Post(**blog_params)

        db.session.add(post)
        db.session.commit()

        return True

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query == '':
            return text('')

        search_query = "%{0}%".format(query)
        print('SEARCH QUERY IS:', search_query)

        post = or_(Post.url.ilike(search_query))
        print('POST SEARCHED IS:', post)
        return post

    @classmethod
    def drafts(cls):
        return Entry.select().where(Post.visible == False)

class Tag(ResourceMixin, db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), unique=True)


# class Post_To_Tag(ResourceMixin, db.Model):
#     post = ForeignKeyField(Post)
#     tag = ForeignKeyField(Tag)

# class Comment(ResourceMixin, db.Model):
#     username = CharField(64)
#     email = CharField()
#     body = CharField(2048)
#     reply_to = ForeignKeyField('self',null=True)