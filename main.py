# main.py

from app import app
from db_setup import init_db, db_session
from forms import SearchForm, ReportForm, LoginForm, RegistrationForm
from flask import flash, render_template, request, redirect, session, url_for, send_from_directory
from models import Report, Nickname, User
from tables import Results
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


init_db()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='error')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm(request.form, csrf_enabled=False)
    if  request.method == 'POST':
        if form.validate():
            Users = User()
            Users.username = form.username.data
            Users.email = form.email.data
            Users.set_password(form.password.data)
            db_session.add(Users)
            db_session.commit()
            flash('Congratulations, you are now a registered user!', category='success')
            return redirect('/')
    return render_template('reg.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/index') 
@login_required
def search_results(search):
    results = []
    search_string = search.data['search']
    if current_user.role == 'user':
        if search_string:
            if search.data['select'] == 'Nickname':
                qry = db_session.query(Report, Nickname).filter(Report.username.contains(current_user.username)).filter(
                    Nickname.id == Report.nickname_id).filter(Nickname.name.contains(search_string))
                results = [item[0] for item in qry.all()]
            elif search.data['select'] == 'Game':
                qry = db_session.query(Report).filter(Report.username.contains(
                    current_user.username)).filter(Report.game_type.contains(search_string))
                results = qry.all()
            elif search.data['select'] == 'ServiceLogin':
                qry = db_session.query(Report).filter(Report.username.contains(current_user.username)).filter(
                    Report.service_login.contains(search_string))
                results = qry.all()
            elif search.data['select'] == 'Incident type':
                qry = db_session.query(Report).filter(Report.username.contains(current_user.username)).filter(
                    Report.incident_type.contains(search_string))
                results = qry.all()
        else:
            qry = db_session.query(Report).filter(
                Report.username.contains(current_user.username))
            results = qry.all()

    if current_user.role == 'admin':
        if search_string:
            if search.data['select'] == 'Nickname':
                qry = db_session.query(Report, Nickname).filter(
                    Nickname.id == Report.nickname_id).filter(Nickname.name.contains(search_string))
                results = [item[0] for item in qry.all()]
            elif search.data['select'] == 'Game':
                qry = db_session.query(Report).filter(
                    Report.game_type.contains(search_string))
                results = qry.all()
            elif search.data['select'] == 'ServiceLogin':
                qry = db_session.query(Report).filter(
                    Report.service_login.contains(search_string))
                results = qry.all()
            elif search.data['select'] == 'Incident type':
                qry = db_session.query(Report).filter(
                    Report.incident_type.contains(search_string))
                results = qry.all()
        else:
            qry = db_session.query(Report)
            results = qry.all()

    if not results:
        flash('No results found!', category='error')
        return redirect('index.html')  
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)  


@app.route('/new_report', methods=['GET', 'POST'])
@login_required
def new_report():  # add new report

    form = ReportForm(request.form)

    if request.method == 'POST' and form.validate():
        # save report
        report = Report()
        save_changes(report, form, new=True)
        flash('Report created successfully!', category='success')
        return redirect('/')

    return render_template('new_report.html', form=form)


def save_changes(report, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    nickname = Nickname()
    nickname.name = form.nickname.data

    report.nickname = nickname
    report.service_login = form.service_login.data
    report.comment = form.comment.data
    report.incident_date = form.incident_date.data
    report.incident_type = form.incident_type.data
    report.game_type = form.game_type.data
    report.priority = form.priority.data
    report.ticket = form.ticket.data  
    report.username = current_user.username
    report.status = form.status.data
    report.resolution = form.resolution.data
    #if current_user.role == 'admin':
    report.comment_soc = form.comment_soc.data
        
    

    if new:
        # Add the new report to the database
        db_session.add(report)

    # commit the data to the database
    db_session.commit()


@app.route('/item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Add / edit an item in the database
    """
    qry = db_session.query(Report).filter(
        Report.id == id)
    report = qry.first()

    if report:
        form = ReportForm(formdata=request.form, obj=report)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(report, form)
            flash('Report updated successfully!', category='success')
            return redirect('/')
        return render_template('edit_report.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(Report).filter(
        Report.id == id)
    report = qry.first()

    if report:
        form = ReportForm(formdata=request.form, obj=report)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(report)
            db_session.commit()

            flash('Report deleted successfully!', category='success')
            return redirect('/')
        return render_template('delete_report.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('admin.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found")


if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = True
    app.run(port=5012)
