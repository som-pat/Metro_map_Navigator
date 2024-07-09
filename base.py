from flask import Flask
sthw = Flask(__name__)

@sthw.route("/")
def run():
    return "{\"message\":\"Hey DEL GTFS ready for deployment,yo rady to rumble\"}"

if __name__ == "__main__":
    sthw.run(host="0.0.0.0", port=int("5000"), debug = True )

