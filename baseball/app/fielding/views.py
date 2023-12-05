from flask import current_app, render_template, request, redirect, url_for, flash
from . import fielding_blueprint as app
from .search import FieldingSearchForm
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

@app.route('/fielding', methods=["GET", "POST"])
@app.route('/fielding/', methods=["GET", "POST"])
def fielding_search():
    form = FieldingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = query_fill(form, current_app.config['FIELDING'])
        return redirect(url_for('fielding.fielding_info', query=query))
    return render_template('fielding.html', form=form, purpose='Search')

@app.route('/fielding/<row_list:query>')
@app.route('/fielding/<row_list:query>/')
def fielding_info(query):
    fielding = current_app.config['FIELDING']
    results = fielding.view_fielding(query)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_search'))
    return render_template('fielding_info.html', query=query, results=paginated_data, header=current_app.config['FIELDING'].HEADER, page_info=page_info)

@app.route('/fielding/<row_list:query_list>/detail')
@app.route('/fielding/<row_list:query_list>/detail/')
def fielding_detail(query_list):
    fielding = current_app.config['FIELDING']
    results = fielding.view_fielding(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_search'))
    return render_template('fielding_detail.html', result=results[0], header=current_app.config['FIELDING'].HEADER)

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
    ret = fielding.update_fielding(transmit, query_list)
    if ret == 0:
        flash(f'Successfully updated!', 'success')
        return render_template('home.html')
    else:
        return redirect(url_for('home.error', message="Update error!"))

@app.route('/fielding/<row_list:query_list>/delete')
@app.route('/fielding/<row_list:query_list>/delete/')
def fielding_delete(query_list):
    fielding = current_app.config['FIELDING']
    fielding.delete_fielding(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')

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
    fielding.insert_fielding(query_list)
    results = fielding.view_fielding(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('fielding.fielding_insert_search'))
    return render_template('fielding_detail.html', result=results[0], header=current_app.config['FIELDING'].HEADER)