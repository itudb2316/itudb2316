from flask import current_app, render_template, request, redirect, url_for, flash
from . import teamshalf_blueprint as app
from .search import TeamshalfSearchForm
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

@app.route('/teamshalf', methods=["GET", "POST"])
@app.route('/teamshalf/', methods=["GET", "POST"])
def teams_search():
    form = TeamshalfSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMSHALF'])
        return redirect(url_for('teamshalf.teamshalf_info', query=query))
    return render_template('teamshalf.html', form=form, purpose='Search')

@app.route('/teamshalf/<row_list:query>')
@app.route('/teamshalf/<row_list:query>/')
def teamshalf_info(query):
    teamshalf = current_app.config['TEAMSHALF']
    results = teamshalf.view_teams(query)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teamshalf.teams_search'))
    return render_template('teamshalf_info.html', query=query, results=paginated_data, header=current_app.config['TEAMSHALF'].HEADER, page_info=page_info)

@app.route('/teamshalf/<row_list:query_list>/detail')
@app.route('/teamshalf/<row_list:query_list>/detail/')
def teamshalf_detail(query_list):
    teamshalf = current_app.config['TEAMSHALF']
    results = teamshalf.view_teams(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teamshalf.teams_search'))

    return render_template('teamshalf.html', result=results[0], header=current_app.config['TEAMSHALF'].HEADER)

@app.route('/teamshalf/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/teamshalf/update/<row_list:transmit>/', methods=["GET", "POST"])
def teams_update_search(transmit):
    form = TeamshalfSearchForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['TEAMSHALF'].HEADER):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMSHALF'])
        return redirect(url_for('teamshalf.teams_update', query_list=query, transmit=transmit))
    return render_template('teamshalf.html', form=form, purpose='Update')

@app.route('/teamshalf/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/teamshalf/<row_list:query_list>/update/<row_list:transmit>/')
def teams_update(query_list, transmit):
    teamshalf = current_app.config['TEAMSHALF']
    teamshalf.update_teams(transmit, query_list)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/teamshalf/<row_list:query_list>/delete')
@app.route('/teamshalf/<row_list:query_list>/delete/')
def teams_delete(query_list):
    teamshalf = current_app.config['TEAMSHALF']
    teamshalf.delete_teams(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/teamshalf/insert', methods=["GET", "POST"])
@app.route('/teamshalf/insert/', methods=["GET", "POST"])
def teams_insert_search():
    form = TeamshalfSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['TEAMSHALF'])
        return redirect(url_for('teamshalf.teams_insert', query_list=query))
    return render_template('teamshalf.html', form=form, purpose='Insertion')

@app.route('/teamshalf/<row_list:query_list>/insert')
@app.route('/teamshalf/<row_list:query_list>/insert/')
def teams_insert(query_list):
    teamshalf = current_app.config['TEAMSHALF']
    teamshalf.insert_teams(query_list)
    results = teamshalf.view_teams(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('teamshalf.teams_insert_search'))
    return render_template('teamshalf_detail.html', result=results[0], header=current_app.config['TEAMSHALF'].HEADER)