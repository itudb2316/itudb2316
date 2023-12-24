from flask import current_app, render_template, request, redirect, url_for, flash
from . import fielding_blueprint as app
from .search import FieldingSearchForm
from app.tools import paginate

def getURLQuery(query, table):
    url_query = {}
    for k, v in query.items():
        #if k in current_app.config[table].COLUMNS.keys():
        if k[0:2] == 'mk' or k[0:2] == 'sc' or k[0:2] == 'mc':
            if v == 'None' or v == None or v == '':
                continue
            
            url_query[k] = v
    return url_query

@app.route('/fielding/search', methods=["GET", "POST"])
def fielding_search():
    form = FieldingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        #read form data into query_params
        query_params = request.form.to_dict()
        query_params.pop('csrf_token')
        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params, "FIELDING")
        print(query_params)
        return redirect(url_for('fielding.fielding_info', **query_params))
    return render_template('fielding.html', form=form, purpose='Search')

@app.route('/fielding/results', methods=["GET", "POST"])
def fielding_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    fielding = current_app.config['FIELDING']
    query = getURLQuery(query, "FIELDING")  # Filter query dictionary to include only column names
    results = fielding.view_fielding(query, sort_by, order)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_search'))
    return render_template('fielding_info.html', query=query, results=paginated_data, 
                            header=current_app.config['FIELDING'].INFO['fielding'], 
                            page_info=page_info, sort_by=sort_by, order=order)

@app.route('/fielding/detail')
def fielding_detail():
    fielding = current_app.config['FIELDING']
    query = request.args.to_dict()
    results = fielding.view_fielding(query)
    print(results[0])

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_search'))
    return render_template('fielding_detail.html', result=results[0], header=current_app.config['FIELDING'].INFO['fielding'])

@app.route('/fielding/update_form', methods=["GET", "POST"])
def fielding_update_search():
    form = FieldingSearchForm()
    fielding = current_app.config['FIELDING']

    for key, _ in fielding.keyvalues.items():
        fielding.keyvalues[key] = request.args.get(key, None, type=str)
    query = {}
    for key, value in fielding.keyvalues.items():
        query[key.lstrip('k')] = value
    field = fielding.view_fielding(query)[0]

    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(fielding.COLUMNS.keys()):
                form.__dict__['_fields'][k].data = field[i]

    if request.method == 'POST' and form.validate_on_submit():
        queries = request.form.to_dict()
        queries.pop('csrf_token')
        print("QUERY_STRING", queries)
        return redirect(url_for('fielding.fielding_update', **fielding.keyvalues, **queries))
    return render_template('fielding.html', form=form, purpose='Update')

@app.route('/fielding/update', methods=["GET", "POST"])
def fielding_update():
    fielding = current_app.config['FIELDING']
    queries = getURLQuery(request.args.to_dict(), "FIELDING")

    for key, _ in fielding.keyvalues.items():
        fielding.keyvalues[key] = request.args.get(key, None, type=str)
    db_response = fielding.update_fielding(queries)

    if db_response == True:
        flash(f'Successfully updated!', 'success')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Update error!"))

@app.route('/fielding/delete')
def fielding_delete():
    fielding = current_app.config['FIELDING']

    for key, _ in fielding.keyvalues.items():
        fielding.keyvalues[key] = request.args.get(key, None, type=str)
    db_response = fielding.delete_fielding()

    if db_response == True:
        flash(f'Successfully deleted!', 'warning')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Deletion error!"))

@app.route('/fielding/insert_form', methods=["GET", "POST"])
def fielding_insert_search():
    form = FieldingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        queries = request.form.to_dict()
        getURLQuery(queries, "FIELDING")
        return redirect(url_for('fielding.fielding_insert', **queries))
    return render_template('fielding.html', form=form, purpose='Insertion')

@app.route('/fielding/insert')
def fielding_insert():
    fielding = current_app.config['FIELDING']
    db_response = fielding.insert_fielding(request.args.to_dict())

    if db_response == True:
        flash(f'Successfully inserted!', 'success')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Insertion error!"))