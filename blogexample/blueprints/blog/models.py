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
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='cascade'), primary_key=True),    ##ORDER IS IMPORTANT!!! 
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='cascade'), primary_key=True)       ##PARENT FIRST, CHILD NEXT
    )


class Post(ResourceMixin, db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    #short_description = db.Column(db.String())
    body = db.Column(db.String(), nullable=False)

    # time = DateTimeField(default=datetime.now)
    url = db.Column(db.String(128), nullable=False, unique=True)
    visible = db.Column(db.Boolean(), index=True, nullable=False, server_default='1')

    # tags_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tags = db.relationship('Tag', secondary=post_tags_table, backref=db.backref('post_tags_table', lazy='dynamic'))
    #tags = db.relationship('Tag', secondary=wiki_tags_table, backref=db.backref('wiki_tags_table', lazy='dynamic'))
    #@staticmethod


    @classmethod
    def create_url(cls, line):
        line = re.sub(r"[^\w\s]", "", line).strip()
        line = line[:64].strip()
        line = line.replace(" ","-").lower()
        return line

    @property
    def tagstring(self):
        return (','.join(tagobj.tag for tagobj in self.tags))
    

    def addTag(self, tag):
        print('TAG IS: ', tag)
        tag = tag.strip().replace(" ","_").lower()
        db_tag = Tag.query.filter(Tag.tag == tag).first()
        print('DB TAG IS: ', db_tag)
        
        if db_tag is None:   
            db_tag = Tag(tag=tag)
            db_tag.save()

        #add to many-to-many table
        #db_post_to_tag = post_tags_table(tag = db_tag,post = self)
        #db_post_to_tag.save()

        self.tags.append(db_tag)
        print('NEW TAG APPENDED TO POST: ', db_tag)
        # db.session.commit()

    #deleting CASCADE EFFECTS: https://docs.sqlalchemy.org/en/13/orm/cascades.html
    def removeTag(self, tag):
        print('TAG IS: ', tag)
        tag = tag.strip().replace(" ","_").lower()
        db_tag = Tag.query.filter(Tag.tag == tag).first()
        print('DB TAG IS: ', db_tag)
        
        self.tags.remove(db_tag)
        print('NEW TAG REMOVED FROM POST: ', db_tag)

    @classmethod
    def string_to_tag_list(cls, tagstring):
        if len(tagstring.replace(",", "").strip()) > 0:
            tags = [x.strip().replace(" ","_") for x in tagstring.split(",") if len(x.strip())>0]
            return tags
        else:
            return None


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
        print('PARAMS ARE: ', params)
        blog_params = {}
        blog_params['title'] = params['title']
        blog_params['body'] = params['body']
        blog_params['visible'] = params['visible']
        blog_params['url'] = Post.create_url(params['title'])

        print('CREATING BLOG POST NOW with params', blog_params)
        post = Post(**blog_params)

        taglist = Post.string_to_tag_list(params['taglist'])
        print('TAGLIST IS: ', taglist)
        if taglist is None:
            post.addTag("untagged")
        else:
            for newtag in taglist:
                post.addTag(newtag)

        db.session.add(post)
        db.session.commit()

        return True

    @classmethod
    def update_blogpost(cls, params):
        """
        Return whether or not the blogpost was created successfully.
        params are in admin/views/coupons_new
        params = {
            'title': coupon.code,
            'body': coupon.duration,
        }
        :return: bool
        """
        print('PARAMS ARE: ', params)
        blog_params = {}
        blog_params['title'] = params['title']
        blog_params['body'] = params['body']
        blog_params['visible'] = params['visible']
        blog_params['url'] = Post.create_url(params['title'])

        print('CREATING BLOG POST NOW with params', blog_params)
        post = Post(**blog_params)

        taglist = Post.string_to_tag_list(params['taglist'])
        print('TAGLIST IS: ', taglist)
        if taglist is None:
            post.addTag("untagged")
        else:
            for newtag in taglist:
                post.addTag(newtag)

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
        return Post.query.filter(Post.visible.is_(False))

    @classmethod
    def published(cls):
        return Post.query.filter(Post.visible)

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