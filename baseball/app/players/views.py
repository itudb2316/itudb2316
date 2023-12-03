from flask import current_app, render_template, request, redirect, url_for, flash
from . import players_blueprint as app
from .search import PlayersSearchForm
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

@app.route('/players', methods=["GET", "POST"])
@app.route('/players/', methods=["GET", "POST"])
def players_search():
    form = PlayersSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('players.players_info', query=query))
    return render_template('players.html', form=form, purpose='Search')

@app.route('/players/<row_list:query>')
@app.route('/players/<row_list:query>/')
def players_info(query):
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)
    
    players = current_app.config['PLAYERS']
    results = players.view_players(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('players.players_search'))
    return render_template('players_info.html', query=query,results=paginated_data,
                            header=current_app.config['PLAYERS'].HEADER, page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/players/<row_list:query_list>/detail')
@app.route('/players/<row_list:query_list>/detail/')
def players_detail(query_list):
    players = current_app.config['PLAYERS']
    results = players.view_players(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('players.players_search'))
    
    return render_template('players_detail.html', result=results[0], header=current_app.config['PLAYERS'].HEADER)

@app.route('/players/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/players/update/<row_list:transmit>/', methods=["GET", "POST"])
def players_update_search(transmit):
    form = PlayersSearchForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['PLAYERS'].HEADER):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('players.players_update', query_list=query, transmit=transmit))
    return render_template('players.html', form=form, purpose='Update')

@app.route('/players/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/players/<row_list:query_list>/update/<row_list:transmit>/')
def players_update(query_list, transmit):
    players = current_app.config['PLAYERS']
    players.update_players(transmit, query_list)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/players/<row_list:query_list>/delete')
@app.route('/players/<row_list:query_list>/delete/')
def players_delete(query_list):
    players = current_app.config['PLAYERS']
    players.delete_players(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/players/insert', methods=["GET", "POST"])
@app.route('/players/insert/', methods=["GET", "POST"])
def players_insert_search():
    form = PlayersSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('players.players_insert', query_list=query))
    return render_template('players.html', form=form, purpose='Insertion')

@app.route('/players/<row_list:query_list>/insert')
@app.route('/players/<row_list:query_list>/insert/')
def players_insert(query_list):
    players = current_app.config['PLAYERS']
    players.insert_players(query_list)
    results = players.view_players(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('players.players_insert_search'))
    return render_template('players_detail.html', result=results[0], header=current_app.config['PLAYERS'].HEADER)