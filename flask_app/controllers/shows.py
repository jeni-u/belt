from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route('/new/show')
def newShow():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('addshow.html',user=user)


@app.route('/create/show', methods=['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')

    if not Show.validate_show(request.form):
        return redirect(request.referrer)

    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }

    Show.createShow(data)
    return redirect('/dashboard')



@app.route('/edit/show/<int:id>')
def editShow(id):
    if 'user_id' not in session:
        return redirect('/')

    show = Show.get_show_by_id(id)
    if not show:
        return redirect('/')
    loggedUser = User.get_user_by_id({'id': session['user_id']})
    if show['user_id'] != loggedUser['id']:
        return redirect('/')

    return render_template('editshow.html', show=show, loggedUser=loggedUser)


@app.route('/update/show/<int:id>', methods=['POST'])
def updateshow(id):
    if 'user_id' not in session:
        return redirect('/')

    show = Show.get_show_by_id(id)
    if not show:
        return redirect('/')
    
    loggedUser = User.get_user_by_id({'id': session['user_id']})
    if not loggedUser:
        return redirect('/')

    if show['user_id'] != loggedUser['id']:
        return redirect('/')

    updateData = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'id': id
    }
    
    if not Show.validate_show(updateData):
        return redirect(request.referrer)

    Show.update_show(updateData)
    return redirect('/dashboard')

    

@app.route('/delete/show/<int:id>')
def delete_show(id):
    if 'user_id' not in session:
        
        return redirect('/')
    
    
    show = Show.get_show_by_id(id)
    if not show:
        flash("Show not found!")
        return redirect('/')
    
    user_id = session['user_id']
    if show['user_id'] != user_id:
        
        return redirect('/')
    
    data = {'show_id': id}
    
    Show.removeLike(data)
    
    Show.delete_show(data)
    
    return redirect(request.referrer)



@app.route('/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'show_id': id,
        'user_id': session['user_id']
    }

    if not Show.has_liked(data):
        Show.like(data)

    return redirect('/dashboard')


@app.route('/removeLike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'show_id': id,
        'user_id': session['user_id'] 
    }
    Show.removeLike(data)
    return redirect('/dashboard')






@app.route('/view/show/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'user_id': session['user_id']
    }

    users_like = Show.allUsers(data)
    likes_count = Show.get_likes_count(data)
    shows = Show.get_show_by_id(id)
    loggedUser = User.get_user_by_id(data)
    return render_template("view.html", shows=shows, loggedUser=loggedUser,users_like=users_like,likes_count=likes_count)

