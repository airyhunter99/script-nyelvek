import json
import jsonschema
import flask
from flask import *

app = flask.Flask(__name__)

if __name__ == "__main__":
    app.run()


@app.route('/', methods=['GET'])
@app.route('/fooldal', methods=['GET'])
def fooldal():
    return render_template('fooldal.html')


@app.route('/etelek')
def etelek():
    return render_template('etelek.html', etelek=json.load(open('etelek.json', encoding="UTF-8")))


@app.route('/etel', methods=['GET'])
def etel():
    azonosito = int(request.args['azonosito'])

    return render_template('etel.html', etel=json.load(open('etelek.json', encoding="UTF-8"))[azonosito - 1])


@app.route('/hozzaad', methods=['POST'])
def uj_etel():
    schema = {
        "type": "object",
        "properties": {
            "azonosito": {"type": "number"},
            "nev": {"type": "string"},
            "ar": {"type": "number"},
            "kaloria": {"type": "number"}
        },
    }

    etelek = json.load(open('etelek.json', encoding="UTF-8"))



    try:
        etel = {
            "azonosito": len(etelek) + 1,
            "nev": request.form["nev"],
            "ar": int(request.form["ar"]),
            "kaloria": int(request.form["kaloria"])
        }

        jsonschema.validate(instance=etel, schema=schema)

        etelek.append(etel)

        with open("etelek.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(etelek, indent=4, ensure_ascii=False))
    except:
        return 'Hibás típus!', 400

    return redirect("/fooldal")