# Criar Rotas
from flask import render_template, url_for, redirect, flash, request
from fakePintrest import app, database as db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakePintrest.forms import FormLogin, FormSignUp, FormPhoto
from fakePintrest.models import User, Photo
import os
from werkzeug.utils import secure_filename

@app.route("/",methods=['GET','POST'])
def homePage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        user = User.query.filter_by(email=formLogin.email.data).first()
        print(user.password)
        print(formLogin.password.data)
        if user and bcrypt.check_password_hash(user.password, formLogin.password.data):
            login_user(user)
            return redirect(url_for('perfil', id_user=user.id))
    return render_template("homePage.html", form=formLogin)

@app.route("/criarconta", methods=['GET', 'POST'])
def createAccount():
    formCreateAccount = FormSignUp()
    if request.method == 'POST':
        print("Formulário enviado")
        if formCreateAccount.validate_on_submit():
            print("Validação do formulário bem-sucedida")
            hashed_password = bcrypt.generate_password_hash(formCreateAccount.password.data).decode('utf-8')
            user = User(username=formCreateAccount.username.data, email=formCreateAccount.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Sua conta foi criada com sucesso!', 'success')
            return redirect(url_for('perfil', id_user=user.id))
        else:
            print("Falha na validação do formulário")
            print(formCreateAccount.errors)
    return render_template('createAccount.html', form=formCreateAccount)

@app.route("/perfil/<id_user>", methods=['GET','POST'])
@login_required
def perfil(id_user):
    if int(id_user) == int(current_user.id):
        form_photo = FormPhoto()
        if form_photo.validate_on_submit():
            arquivo = form_photo.foto.data
            secure_name = secure_filename(arquivo.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"],
                                secure_name)
            arquivo.save(path)
            photo = Photo(image=secure_name, user_id = id_user)
            db.session.add(photo)
            db.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_photo)
    else:
        usuario = User.query.get(int(id_user))
        if usuario:
            return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/feed")
def feed():
    photos = Photo.query.order_by(Photo.create_date).all()
    return render_template("feed.html", fotos=photos)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homePage'))