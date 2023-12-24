from flask import current_app, render_template, request, redirect, url_for, flash
from . import batting_blueprint as app
from app.tools import paginate
from .search import BattingSearchForm

def get_url_query(data):
    url_query = {}
    for k, v in data.items():
        if k in current_app.config['BATTING'].header_type.keys():
            if v == None or v == 'None' or v == '':
                continue
            url_query[k] = v
    return url_query

def filled_query(form, table):
    
    query = []
    
    for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
        if i < len(table.header):
            query.append(form.__dict__['_fields'][k].data)
    for i in range(len(query)):
        if type(query[i]) == str:
            if query[i] == '':
                query[i] = 'None'
        elif type(query[i]) == int:
            if query[i] < 0:
                query[i] = 'None'
    return query

@app.route('/batting/search', methods=["GET", "POST"])
def batting_search():
    form = BattingSearchForm() 
    if request.method == 'POST' and form.validate_on_submit():
        query_parameters = request.form.to_dict()
        query_parameters = get_url_query(query_parameters)
        print(query_parameters)
        return redirect(url_for('batting.batting_info', **query_parameters))
    return render_template('batting.html', form = form, purpose='Search')

@app.route('/batting/results', methods=["GET", "POST"]) 
def batting_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)
    batting = current_app.config['BATTING']
    query = get_url_query(query)
    results = batting.view_batting(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page,'pages': pages}
    
    Titles = ["Player", "Year", "Stint", "Team", "League", "Games", "At Bats",
              "Runs", "Hits", "Doubles", "Triples", "Home Runs", "Runs Batted In",
              "Stolen Bases", "Caught Stealing", "Strikeouts"]
    
    if len(results) == 0:
        flash(f'No results were found.', 'danger')
        return redirect(url_for('batting.batting_search'))
    return render_template('batting_info.html', query = query,results=paginated_data, header=Titles, page_info=page_info, sort_by=sort_by, order=order)

@app.route('/batting/detail')
def batting_detail():
    query = request.args.to_dict()
    query = get_url_query(query)
    batting = current_app.config['BATTING']
    results = batting.view_batting(query)
    if len(results) == 0:
        flash(f'No results were found.', 'danger')
        return redirect(url_for('batting.batting_search'))
    return render_template('batting_detail.html', result=results[0], header=list(current_app.config['BATTING'].header_type.keys()))
    
    
@app.route('/batting/insert_form', methods=["GET", "POST"])
def batting_insert_search():
    form = BattingSearchForm()
    battings = current_app.config['BATTING']
    if request.method == 'POST' and form.validate_on_submit():
        query_string = "&".join(f"{list(battings.header_type.keys())[i]}={form.__dict__['_fields'][k].data}"
                                 for i, (k, _) in enumerate(form.__dict__['_fields'].items())
                                   if form.__dict__['_fields'][k].data != '' and i < len(battings.header_type.keys() ))
        print("QUERY STRING: ", query_string)
        return redirect(url_for('batting.batting_insert')+f'?{query_string}')
    return render_template('batting.html', form=form, purpose='Insertion')

@app.route('/batting/insert', methods=["GET", "POST"])
def batting_insert():
    battings = current_app.config['BATTING']
    queries = get_url_query(request.args.to_dict())
    battings.insert_batting(queries)
    results = battings.view_batting(queries)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('batting.batting_insert_search'))
    return render_template('batting_detail.html', result=results[0], header=list(current_app.config['BATTING'].header_type.keys()))

@app.route('/batting/update_form', methods=["GET", "POST"])
def batting_update_search():
    form = BattingSearchForm()
    battings = current_app.config['BATTING']
    key1 = request.args.get('playerID', None, type=str)
    key2 = request.args.get('yearID', None, type=str)
    key3 = request.args.get('stint', None, type=str)
    query = {'playerID': key1,
             'yearID': key2,
             'teamID': key3}
    batting_1 = battings.view_batting(query)[0]
    batting_2 = battings.view_batting(query)[1]
    batting_3 = battings.view_batting(query)[2]
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['BATTING'].header_type.keys()):
                form.__dict__['_fields'][k].data = batting_1[i]
                form.__dict__['_fields'][k].data = batting_2[i]
                form.__dict__['_fields'][k].data = batting_3[i]
    
    
    if request.method == 'POST' and form.validate_on_submit():
        query_string = "&".join(f"{list(current_app.config['BATTING'].header_type.keys())[i]}={form.__dict__['_fields'][k].data}" for i, (k, _) in enumerate(form.__dict__['_fields'].items()) if form.__dict__['_fields'][k].data != '' and i < len(current_app.config['BATTING'].header_type.keys() ))
    #Change here for the URL path.
    
    print("QUERY STRING", query_string)
    return redirect(url_for('batting.batting_update') + f'?key1={key1}&key2={key2}&key3={key3}')

@app.route('/batting/update') #To be fixed.
def batting_update(query_list, transmit):
    battings = current_app.config['BATTING']
    key1 = request.args.get('playerID', None, type=str)
    key2 = request.args.get('yearID', None, type=str)
    key3 = request.args.get('stint', None, type=str)
    keys = [key1, key2, key3]
    queries = get_url_query(request.args.to_dict())
    battings.update_batting(keys, queries)
    flash(f'Update successful.', 'success')
    return render_template('home.html')
    

@app.route('/batting/delete')
def batting_delete():
    batting = current_app.config['BATTING']
    key = request.args.get('key', None, type=str)
    batting.delete_batting(key)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')