# api/index.py
import json
from http.server import BaseHTTPRequestHandler
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Get the query params from the request, c
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Extract the names from the query parameters (could be multiple 'name' keys)
        names = query.get('name', [])
        
        marks = []
        for student in student_marks:
            if student['name'] in names:
                marks.append(student['marks'])
        
        # Return the marks as a JSON object
        response = {"marks": marks}
        self.wfile.write(json.dumps(response).encode())
        return
    

student_marks = [{"name":"M","marks":6},{"name":"iPvCFcvb","marks":38},{"name":"hny","marks":78},{"name":"dG","marks":25},{"name":"JISradx1","marks":88},{"name":"iAWonA","marks":53},{"name":"JGeaQ","marks":44},{"name":"z54b5wGv","marks":9},{"name":"Lmfv","marks":43},{"name":"1ms5JVSx","marks":18},{"name":"ndzXV","marks":86},{"name":"0NjG2p","marks":55},{"name":"UOt7FA","marks":30},{"name":"NnNQj","marks":10},{"name":"yyCrm","marks":67},{"name":"kL3EmwUJ1","marks":84},{"name":"KHjbCsBs","marks":62},{"name":"afDEj","marks":2},{"name":"IES6O","marks":59},{"name":"D3vV5ANNt","marks":44},{"name":"Jq","marks":7},{"name":"Mog","marks":17},{"name":"vOUKYxC6S","marks":90},{"name":"dJ0SZZ","marks":62},{"name":"k3DfOnfgl","marks":35},{"name":"zbjs","marks":70},{"name":"h0Qzdi5fhC","marks":23},{"name":"8hN7p","marks":22},{"name":"9r","marks":20},{"name":"Gelnll4dI","marks":38},{"name":"FtOey","marks":19},{"name":"XwJYLVd","marks":48},{"name":"QUM35","marks":31},{"name":"ye","marks":39},{"name":"9RSpupEtIl","marks":92},{"name":"b8","marks":36},{"name":"05t0O","marks":24},{"name":"gNx8","marks":28},{"name":"w4","marks":89},{"name":"ORDGGE4","marks":4},{"name":"kt","marks":90},{"name":"Bh","marks":36},{"name":"pOj9F","marks":8},{"name":"NtZkdtsSbt","marks":2},{"name":"Q4Fvw3S","marks":32},{"name":"1zyx7wMcge","marks":84},{"name":"b1mwV85","marks":55},{"name":"oOIcpWEbQN","marks":46},{"name":"l5","marks":74},{"name":"b0ipbw","marks":7},{"name":"1eONTw","marks":10},{"name":"MEcYYREwwC","marks":58},{"name":"14","marks":41},{"name":"uMhkISFoiM","marks":58},{"name":"6ld8Ib","marks":89},{"name":"Z4","marks":95},{"name":"caR0x","marks":93},{"name":"YUqYWruryD","marks":99},{"name":"hzXRLKu39","marks":74},{"name":"IN","marks":15},{"name":"gd","marks":70},{"name":"uBk1yj","marks":79},{"name":"S1Fl79l2x","marks":38},{"name":"6fy","marks":19},{"name":"HjO0i9TO","marks":65},{"name":"1WYWtIeC","marks":77},{"name":"xkE5boVbT","marks":73},{"name":"S9COB","marks":93},{"name":"S7ob","marks":36},{"name":"6","marks":19},{"name":"75V","marks":99},{"name":"fvwooPqhX","marks":41},{"name":"JeRw0","marks":41},{"name":"xwrRYOCr","marks":1},{"name":"WwAFRYXw0","marks":45},{"name":"jw","marks":43},{"name":"aUCcXOuh","marks":7},{"name":"Cx","marks":40},{"name":"RWh","marks":5},{"name":"zGa","marks":65},{"name":"Rs8a","marks":41},{"name":"Wkt","marks":97},{"name":"xiZqMhiz","marks":90},{"name":"wm","marks":64},{"name":"uH91TQZdU","marks":49},{"name":"ex","marks":18},{"name":"zadtQ","marks":34},{"name":"HPxU","marks":30},{"name":"SNQnE","marks":54},{"name":"Uc1dR5","marks":44},{"name":"WR9RiJ5","marks":7},{"name":"lCSj","marks":61},{"name":"0qTHoWShFK","marks":87},{"name":"z2Ynv4dOnn","marks":87},{"name":"Q3zsl0","marks":84},{"name":"2RItfQoLS","marks":85},{"name":"S","marks":55},{"name":"Wk9cn4mf","marks":55},{"name":"83C5bq","marks":27},{"name":"VErxc","marks":71}]