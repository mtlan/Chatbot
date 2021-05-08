import json
from flask import Flask, request

app = Flask(__name__)
@app.route("/")                   # at the end point /
def hello():                      # call method hello
    req = request.get_json(silent=True, force=True)
    query_response = req["queryResult"]
    print("Request:\n", json.dumps(req, indent=4))
    if query_response.get("action") == "user_name":
        r = query_response.get("parameters")
        r1 = r.get("given-name")
        global name
        name = r1
        print("Patient Name:",name)

if __name__ == "__main__":
                            # on running python app.py
    app.run()                       # run the flask app thêm mới phải tắt chạy lạis
    # app.run(debug=True)

# res = makeWebhookResult(req)
# res = json.dumps(res, indent=4)
# #print(res)
# r = make_response(res)
# r.headers['Content-Type'] = 'application/json'