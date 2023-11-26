from werkzeug.routing import BaseConverter

class RowListConverter(BaseConverter):
    def __init__(self, url_map, randomify=False):
        super(RowListConverter, self).__init__(url_map)
        self.randomify = randomify
        #self.regex = '(\w+)(?:,|$)'

    #val1,val2,...
    def to_python(self, value):
        val_list = []
        for x in value.split(','):
            val_list.append(x)
        return val_list

    def to_url(self, value):
        url_str = ''
        for val in value:
            url_str += str(val) + ','
        url_str = url_str.removesuffix(',')
        return url_str

def paginate(data, page, per_page):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_data = data[start_index:end_index]
    return paginated_data


def list2dict(query_list, header):
    query_dict = {}
    for i in range(len(header)):
        query_dict.update({header[i] : query_list[i]})
    return query_dict

