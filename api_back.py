import bd_connector
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = bottle.Bottle()

@enable_cors
@app.route('/api/classifier/', method=['POST'])
def get_classifier():
    return "OK"





app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)