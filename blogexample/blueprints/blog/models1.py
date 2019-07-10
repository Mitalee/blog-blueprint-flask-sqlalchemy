import datetime
import string
# from collections import OrderedDict
from random import choice

import pytz
from sqlalchemy import or_, and_, text

from sqlalchemy.ext.hybrid import hybrid_property

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from lib.money import cents_to_dollars, dollars_to_cents
from blogexample.app import db

class Post(ResourceMixin, db.Model):
    # DURATION = OrderedDict([
    #     ('forever', 'Forever'),
    #     ('once', 'Once'),
    #     ('repeating', 'Repeating')
    # ])

    # PLAN = OrderedDict([
    #     ('bronze', 'Bronze'),
    #     ('gold', 'Gold'),
    #     ('platinum', 'Platinum')
    # ])

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128))
    slug = db.Column(db.String(128), unique=True)
    content = db.Column(db.String())
    published = db.Column(db.Boolean(), index=True, nullable=False, server_default='1')

    # duration = db.Column(db.Enum(*DURATION, name='duration_types'),
    #                      index=True, nullable=False, server_default='forever')
    # plan_for = db.Column(db.Enum(*PLAN, name='plan_types'),
    #                      index=True, nullable=False, server_default='bronze')

    # redeem_by = db.Column(AwareDateTime(), index=True)


    # def __init__(self, **kwargs):
    #     if self.code:
    #         self.code = self.code.upper()
    #     else:
    #         self.code = Coupon.random_coupon_code()

    #     # Call Flask-SQLAlchemy's constructor.
    #     super(Coupon, self).__init__(**kwargs)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub(r'[^\w]+', '-', self.title.lower())
        ret = super(Post, self).save(*args, **kwargs)

        # Store search content.
        self.update_search_index()
        return ret

    def update_search_index(self):
        search_content = '\n'.join((self.title, self.content))
        try:
            fts_entry = FTSEntry.get(FTSEntry.docid == self.id)
        except FTSEntry.DoesNotExist:
            FTSEntry.create(docid=self.id, content=search_content)
        else:
            fts_entry.content = search_content
            fts_entry.save()


class FTSEntry(FTSModel):
    content = SearchField()

    class Meta:
        database = database


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

        search_query = '%{0}%'.format(query)

        return or_(Coupon.code.ilike(search_query))

    # @classmethod
    # def bulk_delete(cls, ids):
    #     """
    #     Override the general bulk_delete method because we need to delete them
    #     one at a time while also deleting them on Stripe.

    #     :param ids: List of ids to be deleted
    #     :type ids: list
    #     :return: int
    #     """
    #     delete_count = 0

    #     for id in ids:
    #         coupon = Coupon.query.get(id)

    #         if coupon is None:
    #             continue

    #         # Delete on Stripe.
    #         stripe_response = PaymentCoupon.delete(coupon.code)

    #         # If successful, delete it locally.
    #         if stripe_response.get('deleted'):
    #             coupon.delete()
    #             delete_count += 1

    #     return delete_count

    @classmethod
    def find_by_code(cls, code):
        """
        Find a coupon by its code.

        :param code: Coupon code to find
        :type code: str
        :return: Coupon instance
        """
        formatted_code = code.upper()
        coupon = Coupon.query.filter(Coupon.redeemable,
                                     Coupon.code == formatted_code).first()

        return coupon
