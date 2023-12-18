from flask import current_app, render_template, request, redirect, url_for, flash
from . import managers_blueprint as app
from .search import ManagersSearchForm
from app.tools import paginate

def getURLQuery(query):
    url_query = {}
    for k, v in query.items():
        if k in current_app.config['MANAGERS'].COLUMNS.keys():
            if v == 'None' or v == None or v == '':
                continue
            
            url_query[k] = v
    return url_query
    

@app.route('/managers/search', methods=["GET", "POST"])
def managers_search():
    form = ManagersSearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        #read form data into query_params
        query_params = request.form.to_dict()

        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)
        print(query_params)
        return redirect(url_for('managers.managers_info', **query_params))
    return render_template('managers.html', form=form, purpose='Search')

@app.route('/managers/results', methods=["GET", "POST"])
def managers_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    managers = current_app.config['MANAGERS']
    
    query = getURLQuery(query)  # Filter query dictionary to include only column names

    results = managers.view_managers(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('managers.managers_search'))
    return render_template('managers_info.html', query = query,results=paginated_data,
                            header=current_app.config['MANAGERS'].COLUMNS.keys(), page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/managers/detail')
def managers_detail():
    query = request.args.to_dict()
    query = getURLQuery(query)  # Filter query dictionary to include only column names
    managers = current_app.config['MANAGERS']
    
    results = managers.view_managers(query)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('managers.managers_search'))
    
    return render_template('managers_detail.html', result=results[0], header=list(current_app.config['MANAGERS'].COLUMNS.keys()))

@app.route('/managers/update_form', methods=["GET", "POST"])
def managers_update_search():
    form = ManagersSearchForm()

    managers = current_app.config['MANAGERS']
    key = request.args.get('key', None, type=str)
    query = {'lahmanID' : key}
    manager = managers.view_managers(query)[0]

    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(managers.COLUMNS.keys()):
                form.__dict__['_fields'][k].data = manager[i]
    if request.method == 'POST' and form.validate_on_submit():

        query_string = "&".join(f"{list(managers.COLUMNS.keys())[i]}={form.__dict__['_fields'][k].data}"
                                 for i, (k, _) in enumerate(form.__dict__['_fields'].items())
                                   if form.__dict__['_fields'][k].data != '' and i < len(managers.COLUMNS.keys() ))
        print("QUERY_STRİNG", query_string)
        return redirect(url_for('managers.managers_update') + f'?key={key}&{query_string}')
    return render_template('managers.html', form=form, purpose='Update')

@app.route('/managers/update')
def managers_update():
    managers = current_app.config['MANAGERS']
    key = request.args.get('key', None, type=str)
    queries = getURLQuery(request.args.to_dict())

    managers.update_managers(key, queries)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/managers/delete')
def managers_delete():
    managers = current_app.config['MANAGERS']
    key = request.args.get('key', None, type=str)

    managers.delete_managers(key)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/managers/insert_form', methods=["GET", "POST"])
def managers_insert_search():
    form = ManagersSearchForm()
    managers = current_app.config['MANAGERS']
    if request.method == 'POST' and form.validate_on_submit():
        query_string = "&".join(f"{list(managers.COLUMNS.keys())[i]}={form.__dict__['_fields'][k].data}"
                                 for i, (k, _) in enumerate(form.__dict__['_fields'].items())
                                   if form.__dict__['_fields'][k].data != '' and i < len(managers.COLUMNS.keys() ))
        print("QUERY_STRİNG", query_string)
        return redirect(url_for('managers.managers_insert')+f'?{query_string}')
    return render_template('managers.html', form=form, purpose='Insertion')

@app.route('/managers/insert', methods=["GET", "POST"])
def managers_insert():
    managers = current_app.config['MANAGERS']
    queries = getURLQuery(request.args.to_dict())
    managers.insert_managers(queries)
    results = managers.view_managers(queries) # results may have multiple rows... #TODO: check if this is the case

    if len(results) == 0:
        flash(f'Error ! Try again.', 'danger')
        return redirect(url_for('managers.managers_insert_search'))
    return render_template('managers_detail.html', result=results[0], header=list(current_app.config['MANAGERS'].COLUMNS.keys()))