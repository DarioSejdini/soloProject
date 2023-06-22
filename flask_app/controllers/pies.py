from flask_app import app
from flask_app.models.user import User
from flask_app.models.pie import pie

from flask import render_template, redirect, session, request, flash

@app.route('/new')
def addPie():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addPie.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/pie', methods = ['POST'])
def createPie():
    if 'user_id' in session:
        if not pie.validate_pie(request.form):
            return redirect(request.referrer)
        data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'user_id': session['user_id']
        }
        pie.save(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/pies/<int:id>')
def editPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        foundPie = pie.get_pie_by_id(data)
        if loggedUser['id'] == foundPie['user_id']:
            return render_template('editPie.html', loggedUser = loggedUser, pie= foundPie)
        return redirect('/dashboard')
    return redirect('/')


@app.route('/show/<int:id>')
def showPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        foundPie = pie.get_pie_by_id(data)
        likedPies = User.get_user_liked_piesId(data)
        pieLiked = foundPie['id'] in likedPies
        print(pieLiked)
        return render_template('show.html', loggedUser = loggedUser, pie= foundPie, pieLiked = pieLiked)
    return redirect('/')



@app.route('/update/pie/<int:id>', methods = ['POST'])
def updatePie(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        foundPie = pie.get_pie_by_id(data1)

        if loggedUser['id'] == foundPie['user_id']:
            if not pie.validate_pie(request.form):
                return redirect(request.referrer)
            data = {
                 'name': request.form['name'],
                 'filling': request.form['filling'],
                 'crust': request.form['crust'],
                 'user_id': session['user_id'],
                 'pie_id': id 
            }
            pie.update(data)
            return redirect('/')
        
        return redirect('/dashboard')
    return redirect('/')


@app.route('/delete/pie/<int:id>')
def deletePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        foundPie=pie.get_pie_by_id(data)
        if loggedUser['id'] == foundPie['user_id']:
            pie.delete(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        
        likedPies = User.get_user_liked_piesId(data)
        if id not in likedPies:
            pie.like(data)
            return redirect(request.referrer)

        return redirect(request.referrer)
    return redirect('/')


@app.route('/dislike/<int:id>')
def dislike(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        pie.dislike(data)
        return redirect(request.referrer)
    return redirect('/')