
from curses import flash
from datetime import datetime
from flask import render_template,flash,request
from flask import request,abort,url_for,redirect
from ..models import User, Pitches, Upvotes,Downvotes,Comments
from .forms import Pitch,Comment,Upvote,Downvote
from flask_login import login_required, current_user
from flask import abort
from .forms import UpdateProfile
from .. import db
from .. import uploads
from . import main

@main.route('/')
def index():
    
    all_pitches = Pitches.query.order_by(Pitches.posted.desc())   
    
    # total_upvotes = Upvotes.get_all_upvotes(pitch_id= Pitches.pid)    
    title = 'Pitches Home'
    
    return render_template('index.html', title=title, pitches= all_pitches )

@main.route('/love')
def love():
    
    love = Pitches.query.filter_by(category = "Love")     
    title='Love Pitches'
    return render_template('love.html', title=title, Love=love)

@main.route('/life')
def life():
    
    life = Pitches.query.filter_by(category = "Life")    
    title='Life Pitches'
    return render_template('life.html', title=title, Life=life)


@main.route('/business')
def business():
    
    business = Pitches.query.filter_by(category = "Business")    
    title='Businesss Pitches'
    return render_template('business.html', title=title, Business=business)


@main.route('/coding')
def coding():
    
    coding = Pitches.query.filter_by(category = "Coding")    
    title='Coding Pitches'
    return render_template('coding.html', title=title, Coding=coding)

@main.route('/finance')
def finance():
    
    finance = Pitches.query.filter_by(category = "Finance")    
    title='Finance Pitches'
    return render_template('business.html', title=title, Business=finance)


@main.route('/pitches/new/', methods =['GET', 'POST'])
@login_required
def new_pitch():
    # mine_upvotes = Upvotes.query.filter_by( pitch_id= Pitches.pid)
    pitch_form = Pitch()
    if pitch_form.validate_on_submit():
        pitch_title = pitch_form.pitch_title.data        
        pitch_descrip = pitch_form.pitch_descrip.data
        user = current_user
        pitch_category = pitch_form.pitch_category.data
        print(current_user._get_current_object().id)
        new_pitch = Pitches(user = current_user , title=pitch_title, description= pitch_descrip,category= pitch_category)
        # save pitch
        db.session.add(new_pitch)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    return render_template('pitches.html', form= pitch_form)
        
        
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    my_pitches = Pitches.get_my_pitches(user.id) 
    print(' #############')
    print(my_pitches)
    print(' #############')
    
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, Pitches=my_pitches)


#a route that will process our form(image/photo upload form) submission request
@main.route('/user/<uname>/update/',methods= ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

#a route that will process our form(image/photo upload form) submission request
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
    
        filename = uploads.save(request.files['photo'])
        path = f'uploads/{filename}'
        user.profile_pic_path = path
        db.session.add(user)
        db.session.commit()
       
    return redirect(url_for('main.profile',uname=uname))


@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = Comment()
    pitch=Pitches.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.Comment_decrip.data

        new_comment = Comments(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comments.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comments.html', form = form, comment = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote_pitch(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    user = current_user
    new_upvote = Upvotes(pitch_u_id=pitch_id, user = current_user)
    
    pitch_upvotes = Upvotes.query.filter_by(pitch_u_id= pitch_id, user_id= current_user.id).first()
    
    chkupvote =Upvotes.query.filter_by(pitch_u_id=pitch_id,user_id =current_user.id).all()
    if len(chkupvote) > 1:
         return  redirect(request.referrer)
    else:
                
        if pitch_upvotes:
            db.session.add(new_upvote)
            db.session.commit()
            return  redirect(request.referrer)        
        else:
            return  redirect(request.referrer)

@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote_pitch(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    user = current_user
    new_downvote = Downvotes(pitch_d_id=pitch_id, user = current_user)
    
    pitch_downvotes = Downvotes.query.filter_by(pitch_d_id= pitch_id, user_id= current_user.id).first()
    
    chk_down_vote =Downvotes.query.filter_by(pitch_d_id=pitch_id,user_id =current_user.id).all()
    if len(chk_down_vote) > 1:
         return  redirect(request.referrer)
    else:
                
        if pitch_downvotes:
            db.session.add(new_downvote)
            db.session.commit()
            return  redirect(request.referrer)        
        else:
            return  redirect(request.referrer)
    
    