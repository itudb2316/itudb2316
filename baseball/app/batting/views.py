from flask import current_app, render_template, request, redirect, url_for, flash
from . import batting_blueprint as app
from app.tools import paginate
from .search import BattingSearchForm

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

@app.route('/batting', methods=["GET", "POST"])
@app.route('/batting/', methods=["GET", "POST"])
def batting_search():
    form = BattingSearchForm() 
    if request.method == 'POST' and form.validate_on_submit():
        query = filled_query(form, current_app.config['BATTING'])
        return redirect(url_for('batting.batting_info', query = query))
    return render_template('batting.html', form = form, purpose='Search')

@app.route('/batting<row_list:query>')
@app.route('/batting<row_list:query>/')
def batting_info(query):
    batting = current_app.config['BATTING']
    results = batting.view_batting(query)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pages = len(results) // per_page + 1
    paginated_data = paginate(results, page, per_page)
    page_info = {'page': page, 'per_page': per_page, 'pages': pages}
    
    if len(results) == 0:
        flash(f'No results were found!', 'danger')
        return(redirect(url_for('batting.batting_search')))
    return render_template('batting_info.html', query=query, results=paginated_data, header = current_app.config['BATTING'].header, page_info=page_info)

@app.route('/batting/<row_list:query_list>/detail')
@app.route('/batting/<row_list:query_list>/detail/')
def batting_detail(query_list):
    batting = current_app.config['BATTING']
    results = batting.view_batting(query_list)
    
    if len(results) == 0:
        flash(f'No results were found!', 'danger')
        return(redirect(url_for('batting.batting_search')))
    return render_template('batting_detail.html', result=results[0], header=current_app.config['BATTING'].header)

@app.route('/batting/insert', methods=["GET", "POST"])
@app.route('/batting/insert/', methods=["GET", "POST"])
def batting_insert_search():
    form = BattingSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = filled_query(form, current_app.config['BATTING'])
        return redirect(url_for('batting.batting_insert', query_list=query))
    return render_template('batting.html', form=form, purpose='Insertion')

@app.route('/batting/<row_list:query_list>/insert')
@app.route('/batting/<row_list:query_list>/insert/')
def batting_insert(query_list):
    batting = current_app.config['BATTING']
    batting.insert_batting(query_list)
    results = batting.view_batting(query_list)

    if len(results) == 0:
        flash(f'No results were found! Try again.', 'danger')
        return redirect(url_for('batting.batting_insert_search'))
    return render_template('batting_detail.html', result=results[0], header=current_app.config['BATTING'].header)

@app.route('/batting/update/<row_list:transmit>', methods=["GET", "POST"])
@app.route('/batting/update/<row_list:transmit>/', methods=["GET", "POST"])
def batting_update_search(transmit):
    form = BattingSearchForm()
    if request.method == 'GET':
        for i, (k, _) in enumerate(form.__dict__['_fields'].items()):
            if i < len(current_app.config['BATTING'].header):
                form.__dict__['_fields'][k].data = transmit[i]
    if request.method == 'POST' and form.validate_on_submit():
        query = filled_query(form, current_app.config['BATTING'])
        return redirect(url_for('batting.batting_update', query_list=query, transmit=transmit))
    return render_template('batting.html', form=form, purpose='Update')

@app.route('/batting/<row_list:query_list>/update/<row_list:transmit>')
@app.route('/batting/<row_list:query_list>/update/<row_list:transmit>/')
def batting_update(query_list, transmit):
    batting = current_app.config['BATTING']
    batting.update_batting(transmit, query_list)
    flash(f'Successfully updated!', 'success')
    return render_template('home.html')

@app.route('/batting/<row_list:query_list>/delete')
@app.route('/batting/<row_list:query_list>/delete/')
def batting_delete(query_list):
    batting = current_app.config['BATTING']
    batting.delete_batting(query_list)
    flash(f'Successfully deleted!', 'warning')
    return render_template('home.html')