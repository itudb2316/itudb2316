from flask import current_app, render_template, request, redirect, url_for, flash
from . import players_blueprint as app
from .search import PlayersSearchForm
from app.tools import paginate

def getURLQuery(query):
    url_query = {}
    for k, v in query.items():
        if k in current_app.config['PLAYERS'].COLUMNS.keys():
            if v == 'None' or v == None or v == '':
                continue
            
            url_query[k] = v
    return url_query
    

@app.route('/players/search', methods=["GET", "POST"])
def players_search():
    form = PlayersSearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        #read form data into query_params
        query_params = request.form.to_dict()

        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)
        print(query_params)
        return redirect(url_for('players.players_info', **query_params))
    return render_template('players.html', form=form, purpose='Search')

@app.route('/players/results', methods=["GET", "POST"])
def players_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    players = current_app.config['PLAYERS']
    
    query = getURLQuery(query)  # Filter query dictionary to include only column names

    results = players.view_players(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('players.players_search'))
    return render_template('players_info.html', query = query,results=paginated_data,
                            header=current_app.config['PLAYERS'].COLUMNS.keys(), page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/players/detail')
def players_detail():
    query = request.args.to_dict()
    query = getURLQuery(query)  # Filter query dictionary to include only column names
    players = current_app.config['PLAYERS']
    
    results = players.view_players(query)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('players.players_search'))
    
    return render_template('players_detail.html', result=results[0], header=list(current_app.config['PLAYERS'].COLUMNS.keys()))

@app.route('/players/update_form', methods=["GET", "POST"])
def players_update_search():
    form = PlayersSearchForm()

    players = current_app.config['PLAYERS']
    key = request.args.get('key', None, type=str)
    query = {'lahmanID' : key}
    player = players.view_players(query)[0]

    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['PLAYERS'].COLUMNS.keys()):
                form.__dict__['_fields'][k].data = player[i]
    if request.method == 'POST' and form.validate_on_submit():

        query_string = "&".join(f"{list(current_app.config['PLAYERS'].COLUMNS.keys())[i]}={form.__dict__['_fields'][k].data}"
                                 for i, (k, _) in enumerate(form.__dict__['_fields'].items()) if form.__dict__['_fields'][k].data != '' and i < len(current_app.config['PLAYERS'].COLUMNS.keys() ))
        print("QUERY_STRİNG", query_string)
        return redirect(url_for('players.players_update') + f'?key={key}&{query_string}')
    return render_template('players.html', form=form, purpose='Update')

@app.route('/players/update')
def players_update():
    players = current_app.config['PLAYERS']
    key = request.args.get('key', None, type=str)
    queries = getURLQuery(request.args.to_dict())

    players.update_players(key, queries)
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