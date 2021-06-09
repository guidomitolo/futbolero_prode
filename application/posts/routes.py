from flask import render_template, url_for, flash, redirect, request, abort
from application import db
from application.posts import bp
from application.posts.forms import  PostForm
from application.posts.models import Post
from application.auth.models import User
from flask_login import current_user, login_required


@bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('¡Has dejado el mensaje', 'success')
        return redirect(url_for('main.debate'))
    return render_template('posts/create_post.html', title='Nuevo Mensaje',
                           form=form, legend='Nuevo Mensaje')


@bp.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template(
        'posts/post.html', 
        post=post, 
        user=User.query.filter_by(id=current_user.id).first()
    )


@bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        flash('¡Has modificado el mensaje!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.body.data = post.body
    return render_template('posts/create_post.html', title='Editar mensaje',
                           form=form, legend='Editar mensaje')


@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('¡Has eliminado el mensaje!', 'success')
    return redirect(url_for('main.index'))