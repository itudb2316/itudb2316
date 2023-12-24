from flask import current_app, render_template, request, redirect, url_for, flash
from . import batting_blueprint as app
from app.tools import paginate
from .search import BattingSearchForm

def get_url_query(query, table):
    url_query = {}
    for k, v in query.items():
        if k[0:2] == 'mk' or k[0:2] == 'sc' or k[0:2] == 'mc':
            if v == 'None' or v == None or v == '':
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
        query_parameters.pop('csrf_token')
        query_parameters = get_url_query(query_parameters, "BATTING")
        print(query_parameters)
        return redirect(url_for('batting.batting_info', **query_parameters))
    return render_template('batting.html', form = form, purpose='Search')

@app.route('/batting/results', methods=["GET", "POST"]) 
def batting_info():
    query = request.args.to_dict()
    print(query)
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)
    batting = current_app.config['BATTING']
    query = get_url_query(query, "BATTING")
    results = batting.view_batting(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page,'pages': pages}
    
    Titles = ["Player", "Year", "Stint", "Team", "League", "Games", "At Bats",
              "Runs", "Hits", "Doubles", "Triples", "Home Runs", "Runs Batted In",
              "Stolen Bases", "Caught Stealing", "Base on Balls", "Strikeouts",
              "Intentional Walks", "Hits by Pitch", "Sacrifice Hits", "Sacrifice Flies",
              "Plays Grounded into Double Play"]
    
    if len(results) == 0:
        flash(f'No results were found.', 'danger')
        return redirect(url_for('batting.batting_search'))
    return render_template('batting_info.html', query = query,results=paginated_data, header=Titles, page_info=page_info, sort_by=sort_by, order=order)

@app.route('/batting/detail')
def batting_detail():
    query = request.args.to_dict()
    print(query)
    batting = current_app.config['BATTING']
    results = batting.view_batting(query)
    if len(results) == 0:
        flash(f'No results were found.', 'danger')
        return redirect(url_for('batting.batting_search'))
    return render_template('batting_detail.html', result=results[0], header=current_app.config['BATTING'].INFO["batting"])
    
    
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
    queries = get_url_query(request.args.to_dict(), "BATTING")
    battings.insert_batting(queries)
    results = battings.view_batting(queries)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('batting.batting_insert_search'))
    return render_template('batting_detail.html', result=results[0], header=current_app.config['BATTING'].INFO["batting"])

@app.route('/batting/update_form', methods=["GET", "POST"])
def batting_update_search():
    form = BattingSearchForm()
    battings = current_app.config['BATTING']
    key1 = request.args.get('playerID', None, type=str)
    key2 = request.args.get('yearID', None, type=str)
    key3 = request.args.get('stint', None, type=str)
    query = {'playerID': key1,
             'yearID': key2,
             'stint': key3}
    batting_1 = battings.view_batting(query)[0]
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['BATTING'].header_type.keys()):
                form.__dict__['_fields'][k].data = batting_1[i]
    
    
    if request.method == 'POST' and form.validate_on_submit():
        query_string = "&".join(f"{list(current_app.config['BATTING'].header_type.keys())[i]}={form.__dict__['_fields'][k].data}" for i, (k, _) in enumerate(form.__dict__['_fields'].items()) if form.__dict__['_fields'][k].data != '' and i < len(current_app.config['BATTING'].header_type.keys() ))
        print("QUERY STRING", query_string)
        return redirect(url_for('batting.batting_update') + f'?key1={key1}&key2={key2}&key3={key3}&{query_string}')
    return render_template('batting.html', form = form, purpose = 'Update')

@app.route('/batting/update', methods=["GET", "POST"]) #To be fixed.
def batting_update():
    battings = current_app.config['BATTING']
    key1 = request.args.get('key1', None, type=str)
    key2 = request.args.get('key2', None, type=str)
    key3 = request.args.get('key3', None, type=str)
    keys = [key1, key2, key3]
    #d = request.args.to_dict()
    #d['playerID'] = d.pop('key1')
    #d['yearID'] = d.pop('key2')
    #d['stint'] = d.pop('key3')
    #print(d)
    print(request.args.to_dict())
    queries = get_url_query(request.args.to_dict())
    print(queries)
    battings.update_batting(keys, queries)
    flash(f'Update successful.', 'success')
    return render_template('home.html')
    

@app.route('/batting/delete')
def batting_delete():
    batting = current_app.config['BATTING']
    key1 = request.args.get('playerID', None, type=str)
    key2 = request.args.get('yearID', None, type=str)
    key3 = request.args.get('stint', None, type=str)
    keys = [key1, key2, key3]
    batting.delete_batting(keys)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')