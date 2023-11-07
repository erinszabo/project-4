"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    control_dist = request.args.get('control_dist', 999, type=float)
    brevet_start_time = request.args.get("brevet_start_time", 999, type=float)
    #start_time = arrow.get(brevet_start_time, 'YYYY-MM-DDTHH:mm') # make the start time an arrow object
    start_time = arrow.get(brevet_start_time)# make the start time an arrow object
    brevet_dist = request.args.get("brevet_dist")

    app.logger.debug("control_dist={}".format(control_dist))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    #open_time = acp_times.open_time(km, 200, arrow.now().isoformat).format('YYYY-MM-DDTHH:mm')
    #close_time = acp_times.close_time(km, 200, arrow.now().isoformat).format('YYYY-MM-DDTHH:mm')

    # add a check here for valid control distance (as outlined in tests)
    open_time = acp_times.open_time(control_dist, brevet_dist, start_time.isoformat).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(control_dist, brevet_dist, start_time.isoformat).format('YYYY-MM-DDTHH:mm')
    # ^ not currently populating the page...
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
