from flask import current_app, render_template, request, redirect, url_for, flash
from . import managers_blueprint as app
from .search import ManagersSearchForm
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

@app.route('/managers', methods=["GET", "POST"])
@app.route('/managers/', methods=["GET", "POST"])
def managers_search():
    form = ManagersSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('managers.managers_info', query=query))
    return render_template('managers.html', form=form, purpose='Search')

@app.route('/managers/<row_list:query>')
@app.route('/managers/<row_list:query>/')
def managers_info(query):
    sort_by = request.args.get('sort_by', None, type=str)
    order = request.args.get('order', None, type=str)
    
    managers = current_app.config['PLAYERS']
    results = managers.view_managers(query, sort_by, order)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('managers.managers_search'))
    return render_template('managers_info.html', query=query,results=paginated_data,
                            header=current_app.config['PLAYERS'].HEADER, page_info=page_info,
                            sort_by=sort_by, order=order)

@app.route('/managers/<row_list:query_list>/detail')
@app.route('/managers/<row_list:query_list>/detail/')
def managers_detail(query_list):
    managers = current_app.config['PLAYERS']
    results = managers.view_managers(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('managers.managers_search'))
    
    return render_template('managers_detail.html', result=results[0], header=current_app.config['PLAYERS'].HEADER)

@app.route('/managers/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/managers/update/<row_list:transmit>/', methods=["GET", "POST"])
def managers_update_search(transmit):
    form = ManagersSearchForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['PLAYERS'].HEADER):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('managers.managers_update', query_list=query, transmit=transmit))
    return render_template('managers.html', form=form, purpose='Update')

@app.route('/managers/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/managers/<row_list:query_list>/update/<row_list:transmit>/')
def managers_update(query_list, transmit):
    managers = current_app.config['PLAYERS']
    managers.update_managers(transmit, query_list)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/managers/<row_list:query_list>/delete')
@app.route('/managers/<row_list:query_list>/delete/')
def managers_delete(query_list):
    managers = current_app.config['PLAYERS']
    managers.delete_managers(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

@app.route('/managers/insert', methods=["GET", "POST"])
@app.route('/managers/insert/', methods=["GET", "POST"])
def managers_insert_search():
    form = ManagersSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['PLAYERS'])
        return redirect(url_for('managers.managers_insert', query_list=query))
    return render_template('managers.html', form=form, purpose='Insertion')

@app.route('/managers/<row_list:query_list>/insert')
@app.route('/managers/<row_list:query_list>/insert/')
def managers_insert(query_list):
    managers = current_app.config['PLAYERS']
    managers.insert_managers(query_list)
    results = managers.view_managers(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('managers.managers_insert_search'))
    return render_template('managers_detail.html', result=results[0], header=current_app.config['PLAYERS'].HEADER)