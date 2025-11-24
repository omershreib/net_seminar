from detection.dashboard.dashboard_tools import compute_state, updater_loop
from detection.system.database.get_latest_data_plane_id import get_latest_data_plane_id
from detection.system.sensor import sensor
from external.bgp_route_table_ftp_upload import bgp_worker
from detection.system.database.mongo_inserter import MongoInserter
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import request, Flask, render_template, url_for
from turbo_flask import Turbo
from threading import Lock
from datetime import datetime, timedelta
from markupsafe import escape
import threading
import os
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# background thread
thread = None
thread_lock = Lock()

# mongodb config
client = MongoClient("mongodb://localhost:27017/")
db = client["network_monitoring"]

# flask config
app = Flask(__name__)
STATIC_DIR = os.path.join(app.root_path, "static", "charts")
app.config['SERVER_NAME'] = 'BGPDashbard'
app.config['SECRET_KEY'] = 'bgphijack'
turbo = Turbo(app)

os.makedirs(STATIC_DIR, exist_ok=True)

# prefix2as configs
prefix2as_csv = r"D:\Documents\open university\netSeminar\source\detection\detection_tools\prefix2as.csv"
prefixes = pd.read_csv(prefix2as_csv)


# def compute_state(traceroute_id: str):
#     """Fetch latest state and generate charts for a given traceroute id."""
#     collection = db["traceroutes"]
#
#     curr_data_plane = collection.find_one({"sensor_id": 2, "_id": ObjectId(f"{traceroute_id}")})
#     if not curr_data_plane:
#         return None
#
#     destination_ip = curr_data_plane["destination_ip"]
#     trace_hops = curr_data_plane["hops"]
#
#     prev_data_plane = collection.find_one(
#         {"destination_ip": destination_ip, "sensor_id": 2, "_id": {"$lt": ObjectId(traceroute_id)}},
#         sort=[("_id", -1)]
#     )
#     next_data_plane = collection.find_one(
#         {"destination_ip": destination_ip, "sensor_id": 2, "_id": {"$gt": ObjectId(traceroute_id)}},
#         sort=[("_id", 1)]
#     )
#
#     # Delay chart
#     print("update delay chart")
#     delay_chart_fig = get_delay_chart(collection)
#     delay_chart_url = save_fig_png(delay_chart_fig, prefix="delay_chart")
#
#     # update BGP table (provided by LocalISP)
#     ftp_pull.pull_bgp_table_from_ftp("detection/dashboard/bgp_table.txt")
#
#     # Control plane chart
#     control_plane_chart_fig, _ = get_control_plane_chart(prefixes)
#     control_plane_chart_url = save_fig_png(control_plane_chart_fig, prefix="control_plane_chart")
#
#     if trace_hops:
#         data_plane_chart_fig, data_plane_hops_to_asn = get_data_plane_chart(trace_hops, prefixes)
#
#         if data_plane_chart_fig:
#             data_plane_chart_url = save_fig_png(data_plane_chart_fig, prefix="data_plane_chart")
#
#         else:
#             data_plane_chart_url = None
#
#     if not trace_hops:
#         data_plane_chart_url = None
#
#     # Annotate hops with ASN
#     for hop in trace_hops:
#         if hop["responded"]:
#             hop_asn = data_plane_hops_to_asn.get(hop["hop_ip"])
#             hop["asn"] = hop_asn if hop_asn else "*"
#
#         if not hop["responded"]:
#             hop["asn"] = '*'
#
#     return {
#         "data_plane": curr_data_plane,
#         "delay_chart_url": delay_chart_url,
#         "control_plane_chart_url": control_plane_chart_url,
#         "data_plane_chart_url": data_plane_chart_url,
#         "prev_id": str(prev_data_plane["_id"]) if prev_data_plane else traceroute_id,
#         "next_id": str(next_data_plane["_id"]) if next_data_plane else traceroute_id,
#         # Timestamp used to bust browser cache on images
#         "ts": int(time.time())
#     }


# def updater_loop():
#     """Background updater that pushes Turbo replaces to the client every 3 minutes."""
#     with app.app_context():
#         while True:
#             time.sleep(60)  # 3 minutes
#             # We refresh based on the currently viewed UUID; if none, skip
#             # For a single-page per UUID, you can derive it from request args during initial render.
#             # Here we choose to refresh the last requested UUID if present; otherwise skip.
#             # In multi-client setups, consider storing per-client UUID in session or pushing channels.
#             traceroute_id = getattr(updater_loop, "last_uuid", None)
#             if not traceroute_id:
#                 continue
#             state = compute_state(traceroute_id)
#             if not state:
#                 continue
#
#             turbo.push(turbo.replace(render_fragments.render_data_plane_fragment(state), target="data-plane"))
#             turbo.push(turbo.replace(render_fragments.render_delay_chart_fragment(state), target="delay-chart"))
#             turbo.push(turbo.replace(render_fragments.render_control_plane_chart_fragment(state),
#                                      target="control_plane-chart"))
#             turbo.push(
#                 turbo.replace(render_fragments.render_data_plane_chart_fragment(state), target="data_plane-chart"))
#             turbo.push(turbo.replace(render_fragments.render_nav_fragment(state, traceroute_id), target="nav-ids"))


def start_updater_thread():
    # Prevent double-start under Flask's debug reloader
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        t = threading.Thread(target=updater_loop.updater_loop, args=(app, turbo), daemon=True)
        t.start()


def save_fig_png(fig, prefix="chart"):
    """Save a Matplotlib figure to a unique PNG under static/charts and return URL path."""
    filename = f"{prefix}.png"
    filepath = os.path.join(STATIC_DIR, filename)
    fig.tight_layout()
    plt.savefig(filepath, format="png", dpi=120)
    plt.close(fig)
    plt.clf()
    return url_for("static", filename=f"charts/{filename}")


@app.route("/", methods=['GET', 'POST'])
def dashboard():
    collection = db["traceroutes"]
    latest_result = get_latest_data_plane_id(collection)

    print(latest_result)
    traceroute_id = request.args.get("uuid", default=ObjectId(f"{latest_result}"))
    state = compute_state.compute_state(db, prefixes, traceroute_id)
    if not state:
        return f"cannot find traceroute (uuid: {escape(traceroute_id)})"

    # Initial full page render
    return render_template(
        "dashboard.html",
        data_plane=state["data_plane"],
        delay_chart_url=state["delay_chart_url"],
        control_plane_chart_url=state["control_plane_chart_url"],
        data_plane_chart_url=state["data_plane_chart_url"],
        prev_id=state["prev_id"],
        next_id=state["next_id"],
        ts=state["ts"]
    )


@app.before_request
def remember_uuid():
    uuid_arg = request.args.get("uuid")
    if uuid_arg:
        updater_loop.last_uuid = uuid_arg


if __name__ == '__main__':
    # run monitor
    monitored_ip = "198.18.1.13"
    sensor_ip = "192.0.0.3"
    start = datetime.now() + timedelta(seconds=5)  # start 5 seconds from now
    end = start + timedelta(hours=3)  # run for 3 hours

    mongo_inserter = MongoInserter()
    mongo_inserter.connect()

    if not mongo_inserter.is_connect:
        exit(1)

    mongo_inserter.start()
    monitor = sensor.TraceMonitor(monitored_ip, sensor_ip, start, end)
    monitor.start()

    ftp_uploader = threading.Thread(target=bgp_worker, daemon=True)
    ftp_uploader.start()

    print("run server")
    start_updater_thread()
    app.run(host='192.0.0.3', debug=True, threaded=True)
