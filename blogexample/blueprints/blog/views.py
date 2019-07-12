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
    return render_template('posts.html', posts=posts)

@blog.route('/blog')
def published():
    posts = Post.published().order_by(Post.updated_on.desc())
    return render_template('posts.html', posts=posts)

@blog.route('/drafts')
def drafts():
    posts = Post.drafts().order_by(Post.updated_on.desc())
    return render_template('posts.html', posts=posts)

@blog.route('/add', methods=['GET', 'POST'])
def add_post():
    blogpost = Post()
    form = AddPostForm(obj=blogpost)

    # print('TAGS ARE: ',type(request.form["tags"]))
    if form.validate_on_submit():
        form.populate_obj(blogpost)
        params = {
                'title': blogpost.title,#request.form['title'],#
                'body': blogpost.body,#request.form['body'],
                'taglist': request.form['taglist'],#string_to_tag_list(blogpost.tags)
                'visible': blogpost.visible
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

    taglist = ','.join(t.tag for t in blogpost.tags) # DO NOT USE TAGSTRING. IT IS A PROPERTY
    #IF WE USE TAGSTRING, IT WON'T ALLOW POPULATING THE OBJECT VIA populate_obj as it is a property.

    print(' STRINGIFIED TAGLIST IS: ', blogpost.tagstring)
    print('BLOGPOST TAGS CURRENTLY ARE: ', blogpost.tags)

    #this is included here so that it can be populated after modification in the form
    blogpost.taglist = taglist 

    form = UpdatePostForm(obj=blogpost)
    # print("FORM IS: ", form)
    # raise
    if form.validate_on_submit():
        form.populate_obj(blogpost)

        taglist = Post.string_to_tag_list(form.taglist.data)
        print('TAGLIST IS: ', taglist)
        if taglist is None:
            blogpost.addTag("untagged")
        else:
            blogpost_tagnames = [t.tag for t in blogpost.tags]
            for newtag in taglist:
                if newtag not in blogpost_tagnames: 
                    print('{0} NEWTAG IS NOT IN BLOGPOST_TAGNAMES'.format(newtag))
                    blogpost.addTag(newtag)
            for oldtag in blogpost_tagnames:
                if oldtag not in taglist:
                    print('{0} OLDTAG IS NOT IN TAGLIST'.format(newtag))
                    blogpost.removeTag(oldtag)

        ##save the blog post only after adding or removing tags from it.
        blogpost.save()

        ####blogresponse ends up being the whole post object
        #blogresponse = blogpost.save()
        #print('BLOGRESPONSE IS: ', blogresponse)
        # if blogresponse:

        flash('Post has been updated successfully.', 'success')
        return redirect(url_for('blog.show_posts'))
  
    return render_template('update.html', form=form, blogpost=blogpost)#, taglist=taglist)


@blog.route('/tag/<tag_requested>')
def view_tag(tag_requested):
    posts = Post.query.filter(Post.tags.any(Tag.tag == tag_requested))
    return render_template('posts.html', posts=posts)

