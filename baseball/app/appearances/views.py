from flask import current_app, render_template, request, redirect, url_for, flash
from . import appearances_blueprint as app
from .search import AppearancesSearchForm
from app.tools import paginate

def getURLQuery(query):
    url_query = {}
    for k, v in query.items():
        if k in current_app.config['APPEARANCES'].COLUMNS.keys():
            if v == 'None' or v == None or v == '':
                continue
            
            url_query[k] = v
    return url_query
    

@app.route('/appearances/search', methods=["GET", "POST"])
def appearances_search():
    form = AppearancesSearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        #read form data into query_params
        query_params = request.form.to_dict()

        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)
        print(query_params)
        return redirect(url_for('appearances.appearances_info', **query_params))
    return render_template('appearances.html', form=form, purpose='Search')

@app.route('/appearances/results', methods=["GET", "POST"])
def appearances_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    appearances = current_app.config['APPEARANCES']
    
    query = getURLQuery(query)  # Filter query dictionary to include only column names

    results = appearances.view_appearances(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('appearances.appearances_search'))
    return render_template('appearances_info.html', query = query,results=paginated_data,
                            header=current_app.config['APPEARANCES'].COLUMNS.keys(), page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/appearances/detail')
def appearances_detail():
    query = request.args.to_dict()
    query = getURLQuery(query)  # Filter query dictionary to include only column names
    appearances = current_app.config['APPEARANCES']

    
    results = appearances.view_appearances(query)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('appearances.appearances_search'))
    
    return render_template('appearances_detail.html', result=results[0], header=list(current_app.config['APPEARANCES'].COLUMNS.keys()))

@app.route('/appearances/update_form', methods=["GET", "POST"])
def appearances_update_search():
    form = AppearancesSearchForm()

    appearances = current_app.config['APPEARANCES']
    key1 = request.args.get('key1', None, type=str)
    key2 = request.args.get('key2', None, type=str)
    key3 = request.args.get('key3', None, type=str)
    query = {'yearID' : key1,
             'teamID' : key2,
            'playerID' : key3 }
    player = appearances.view_appearances(query)[0]

    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(appearances.COLUMNS.keys()):
                form.__dict__['_fields'][k].data = player[i]
    if request.method == 'POST' and form.validate_on_submit():

        query_params = request.form.to_dict()

        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)

        return redirect(url_for('appearances.appearances_update',**query_params) + f'&key1={key1}&key2={key2}&key3={key3}')
    return render_template('appearances.html', form=form, purpose='Update')

@app.route('/appearances/update')
def appearances_update():
    appearances = current_app.config['APPEARANCES']
    key1 = request.args.get('key1', None, type=str)
    key2 = request.args.get('key2', None, type=str)
    key3 = request.args.get('key3', None, type=str)
    queries = getURLQuery(request.args.to_dict())

    appearances.update_appearances(key1, key2, key3, queries)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/appearances/delete')
def appearances_delete():
    appearances = current_app.config['APPEARANCES']
    key1 = request.args.get('key1', None, type=str)
    key2 = request.args.get('key2', None, type=str)
    key3 = request.args.get('key3', None, type=str)


    appearances.delete_appearances(key1,key2, key3)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/appearances/insert_form', methods=["GET", "POST"])
def appearances_insert_search():
    form = AppearancesSearchForm()
    appearances = current_app.config['APPEARANCES']
    if request.method == 'POST' and form.validate_on_submit():
        query_params = request.form.to_dict()

        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)

        return redirect(url_for('appearances.appearances_insert',**query_params))
    return render_template('appearances.html', form=form, purpose='Insertion')

@app.route('/appearances/insert', methods=["GET", "POST"])
def appearances_insert():
    appearances = current_app.config['APPEARANCES']
    queries = getURLQuery(request.args.to_dict())
    appearances.insert_appearances(queries)
    results = appearances.view_appearances(queries) # results may have multiple rows... #TODO: check if this is the case

    if len(results) == 0:
        flash(f'Error ! Try again.', 'danger')
        return redirect(url_for('appearances.appearances_insert_search'))
    return render_template('appearances_detail.html', result=results[0], header=list(current_app.config['APPEARANCES'].COLUMNS.keys()))