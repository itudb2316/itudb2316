from flask import current_app, render_template, request, redirect, url_for, flash
from . import fielding_blueprint as app
from .search import FieldingSearchForm
from app.tools import paginate

def getURLQuery(query):
    url_query = {}
    for k, v in query.items():
        if k in current_app.config['FIELDING'].COLUMNS.keys():
            if v == 'None' or v == None or v == '':
                continue
            
            url_query[k] = v
    return url_query

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

@app.route('/fielding/search', methods=["GET", "POST"])
def fielding_search():
    form = FieldingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        #read form data into query_params
        query_params = request.form.to_dict()

        print(query_params)
        #remove empty fields and non-column fields and None values
        query_params = getURLQuery(query_params)
        print(query_params)
        return redirect(url_for('fielding.fielding_info', **query_params))
    return render_template('fielding.html', form=form, purpose='Search')

@app.route('/fielding/results', methods=["GET", "POST"])
def fielding_info():
    query = request.args.to_dict()
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)

    fielding = current_app.config['FIELDING']
    query = getURLQuery(query)  # Filter query dictionary to include only column names
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
                            header=current_app.config['FIELDING'].COLUMNS.keys(), 
                            page_info=page_info, sort_by=sort_by, order=order)

@app.route('/fielding/detail')
def fielding_detail():
    fielding = current_app.config['FIELDING']
    query = request.args.to_dict()
    results = fielding.view_fielding(query)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_search'))
    return render_template('fielding_detail.html', result=results[0], header=list(current_app.config['FIELDING'].COLUMNS.keys()))

@app.route('/fielding/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/fielding/update/<row_list:transmit>/', methods=["GET", "POST"])
def fielding_update_search(transmit):
    form = FieldingSearchForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['FIELDING'].HEADER):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['FIELDING'])
        return redirect(url_for('fielding.fielding_update', query_list=query, transmit=transmit))
    return render_template('fielding.html', form=form, purpose='Update')

@app.route('/fielding/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/fielding/<row_list:query_list>/update/<row_list:transmit>/')
def fielding_update(query_list, transmit):
    fielding = current_app.config['FIELDING']
    db_response = fielding.update_fielding(transmit, query_list)
    if db_response == True:
        flash(f'Successfully updated!', 'success')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Update error!"))

@app.route('/fielding/<row_list:query_list>/delete')
@app.route('/fielding/<row_list:query_list>/delete/')
def fielding_delete(query_list):
    fielding = current_app.config['FIELDING']
    db_response = fielding.delete_fielding(query_list)

    if db_response == True:
        flash(f'Successfully deleted!', 'warning')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Deletion error!"))

@app.route('/fielding/insert', methods=["GET", "POST"])
@app.route('/fielding/insert/', methods=["GET", "POST"])
def fielding_insert_search():
    form = FieldingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['FIELDING'])
        return redirect(url_for('fielding.fielding_insert', query_list=query))
    return render_template('fielding.html', form=form, purpose='Insertion')

@app.route('/fielding/<row_list:query_list>/insert')
@app.route('/fielding/<row_list:query_list>/insert/')
def fielding_insert(query_list):
    fielding = current_app.config['FIELDING']
    db_response = fielding.insert_fielding(query_list)

    if db_response == True:
        flash(f'Successfully inserted!', 'success')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Insertion error!"))