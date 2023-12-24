from flask import current_app, render_template, request, redirect, url_for, flash
from . import teams_blueprint as app
from .search import TeamsSearchForm, TeamsInsertionForm, TeamsUpdateForm
from app.tools import paginate

def query_fill(form, table):
    query = []
    for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
        if i < len(table.HEADER):
            query.append(form.__dict__['_fields'][k].data)
    for i in range(len(query)):
        if type(query[i]) == str:
            if query[i] == '':
                query[i] = 'None'
        elif type(query[i]) == int:
            if query[i] < 0:
                query[i] = 'None'
    return query

@app.route('/teams', methods=["GET", "POST"])
@app.route('/teams/', methods=["GET", "POST"])
def teams_search():
    form = TeamsSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMS'])
        return redirect(url_for('teams.teams_info', query=query))
    return render_template('teams.html', form=form, purpose='Search')

@app.route('/teams/<row_list:query>')
@app.route('/teams/<row_list:query>/')
def teams_info(query):
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    teams = current_app.config['TEAMS']
    results = teams.view_teams(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teams.teams_search'))
    return render_template('teams_info.html', query=query,results=paginated_data,
                            header=current_app.config['TEAMS'].HEADER, page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/teams/<row_list:query_list>/detail')
@app.route('/teams/<row_list:query_list>/detail/')
def teams_detail(query_list):
    teams = current_app.config['TEAMS']
    results = teams.view_teams(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teams.teams_search'))

    return render_template('teams_detail.html', result=results[0], header=current_app.config['TEAMS'].HEADER)

@app.route('/teams/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/teams/update/<row_list:transmit>/', methods=["GET", "POST"])
def teams_update_search(transmit):
    form = TeamsUpdateForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['TEAMS'].HEADER):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMS'])
        return redirect(url_for('teams.teams_update', query_list=query, transmit=transmit))
    return render_template('teams.html', form=form, purpose='Update')

@app.route('/teams/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/teams/<row_list:query_list>/update/<row_list:transmit>/')
def teams_update(query_list, transmit):
    teams = current_app.config['TEAMS']
    teams.update_teams(transmit, query_list)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/teams/<row_list:query_list>/delete')
@app.route('/teams/<row_list:query_list>/delete/')
def teams_delete(query_list):
    teams = current_app.config['TEAMS']
    teams.delete_teams(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/teams/insert', methods=["GET", "POST"])
@app.route('/teams/insert/', methods=["GET", "POST"])
def teams_insert_search():
    form = TeamsInsertionForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMS'])
        return redirect(url_for('teams.teams_insert', query_list=query))
    return render_template('teams.html', form=form, purpose='Insertion')

@app.route('/teams/<row_list:query_list>/insert')
@app.route('/teams/<row_list:query_list>/insert/')
def teams_insert(query_list):
    teams = current_app.config['TEAMS']
    teams.insert_teams(query_list)
    results = teams.view_teams(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teams.teams_insert_search'))
    return render_template('teams_detail.html', result=results[0], header=current_app.config['TEAMS'].HEADER)