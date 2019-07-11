#from example.app import create_celery_app, socketio
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import text

from . import blog
from .models import Post, Tag, post_tags_table
from .forms import AddPostForm, UpdatePostForm


@blog.route('/')
def index():
    return render_template('index.html')


@blog.route('/posts')
def show_posts():
    # if session['user_available']:
    #     posts = Posts.query.all()
    #     user = User.query.all()
    #     return render_template('posts.html', posts=posts, user=user)
    # flash('User is not Authenticated')
    # return redirect(url_for('index'))
    posts = Post.query.all()
    print('ALL POSTS ARE', posts)
    return render_template('posts.html', posts=posts)

@blog.route('/blog')
def published():
    posts = Post.published().order_by(Post.updated_on.desc())
    #return object_list('index.html', query)
    return render_template('posts.html', posts=posts)

@blog.route('/drafts')
def drafts():
    posts = Post.drafts().order_by(Post.updated_on.desc())
    #return object_list('index.html', query)
    return render_template('posts.html', posts=posts)

@blog.route('/add', methods=['GET', 'POST'])
def add_post():
    # if session['user_available']:
    #     blogpost = AddPostForm(request.form)
    #     us = User.query.filter_by(username=session['current_user']).first()
    #     if request.method == 'POST':
    #         bp = Posts(blogpost.title.data, blogpost.description.data, us.uid)
    #         db.session.add(bp)
    #         db.session.commit()
    #         return redirect(url_for('show_posts'))
    #     return render_template('add.html', blogpost=blogpost)
    # flash('User is not Authenticated')
    # return redirect(url_for('index'))
    blogpost = Post()
    form = AddPostForm(obj=blogpost)

    # print('TAGS ARE: ',type(request.form["tags"]))
    if form.validate_on_submit():
        # form.populate_obj(blogpost)
        params = {
                'title': request.form['title'],#blogpost.title,
                'body': request.form['body'],#blogpost.body,
                'tags': request.form['tags']#string_to_tag_list(blogpost.tags)
                }
        print('PARAMS ARE: ', params)
        if Post.create_blogpost(params):
            flash('Post has been created successfully.', 'success')
            return redirect(url_for('blog.show_posts'))

    return render_template('add.html', form=form, blogpost=blogpost)


@blog.route('/detail/<url>')
def detail(url):
    #####WORKING
    # search_query = "%{0}%".format(url)
    # print('SEARCH QUERY IS: ', search_query)
    # blogpost = Post.query.filter(Post.url.ilike(search_query)).first()

    blogpost = Post.query.filter(Post.search(url)).first()
    print('TAGS ARE: ', blogpost.tags)

    # print('BLOGPOST IS ', blogpost)
    # flash('Post has been shown successfully.', 'success')
    return render_template('detail.html', blogpost=blogpost)#, tags=tags)

@blog.route('/delete/<pid>', methods=('GET', 'POST'))
def delete_post(pid):
    post = Post.query.get(pid)
    print('POST IS', post)
    del_response = post.delete()
    print(del_response)
    if del_response is None:
        flash('Post has been deleted successfully.', 'success')
    else:
        flash('Error deleting post.', 'danger')   
    return redirect(url_for('blog.show_posts'))


@blog.route('/update/<pid>', methods=('GET', 'POST'))
def update_post(pid):
    blogpost = Post.query.get(pid)
    print('TAGS ARE: ', type(blogpost.tags))
    # taglist = ''
    # for tag in blogpost.tags:
    #     # print('TAG IS: ', tag.tag)
    #     # ','.join(tag.tag)
    #     taglist = taglist+', '+tag.tag

    taglist = ''.join(t.tag for t in blogpost.tags)

    print('TAGLIST IS: ', taglist)

    # blogpost.tags = taglist
    print('BLOGPOST TAGS NOW ARE: ', blogpost.tags)
    blogpost.taglist = taglist
    form = UpdatePostForm(obj=blogpost)

    if form.validate_on_submit():
        # blogpost = User.query.get(request.form.get('id'))
        form.populate_obj(blogpost)

        blogresponse = blogpost.save()
        print('BLOGRESPONSE IS: ', blogresponse)
        if blogresponse:
            flash('Post has been updated successfully.', 'success')
            return redirect(url_for('blog.show_posts'))

    return render_template('update.html', form=form, blogpost=blogpost)#, taglist=taglist)


@blog.route('/tag/<tag>')
def view_tag(tag):
    try:
        tag_id = Tag.get(Tag.tag == tag.lower())
    except Tag.DoesNotExist:
        return render_posts(None, tag = tag.lower())

    posts = [x.post for x in post_tags_table.select().where(post_tags_table.tag == tag_id).join(Post).where(Post.visible == True).order_by(Post.time.desc()) ]

    return render_posts(posts, tag = tag.lower())

def string_to_tag_list(string):
    if len(string.replace(",", "").strip()) > 0:
        tags = [x.strip().replace(" ","_") for x in string.split(",") if len(x.strip())>0]
        return tags
    else:
        return []
def tag_list_to_string(taglist):
    for tag in taglist:
        ''.join(", "+tag)

# def tag(post):
#     if validate_form_field(request.form,"tags"):
#         tags = request.form["tags"]
#         if len(tags.replace(",","").strip())>0:
#             tags = [ x.strip() for x in tags.split(",") if len(x.strip())>0]
#             for tag in tags:
#                 post.addTag(tag)
#         else:
#             post.addTag("untagged")
#     else:
#         post.addTag("untagged")

# def validate_form_field(form,field):
#     return True if len(form[field].strip()) > 0 else False
