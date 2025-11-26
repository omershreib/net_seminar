from config import CONFIG
from detection.dashboard.render_fragments import render_fragments
from detection.dashboard.tools import compute_state
import time

UPDATER_LOOP_SLEEP_TIME = CONFIG['system']['flask_app']['updater_loop_sleep_time']


def updater_loop(app, turbo):
    """Background updater that pushes Turbo replaces to the client every 3 minutes."""
    with app.app_context():
        while True:
            time.sleep(UPDATER_LOOP_SLEEP_TIME)
            traceroute_id = getattr(updater_loop, "last_uuid", None)

            if not traceroute_id:
                continue

            state = compute_state(traceroute_id)

            if not state:
                continue

            turbo.push(turbo.replace(render_fragments.render_data_plane_fragment(state),
                                     target="data-plane"))
            turbo.push(turbo.replace(render_fragments.render_delay_chart_fragment(state),
                                     target="delay-chart"))
            turbo.push(turbo.replace(render_fragments.render_control_plane_chart_fragment(state),
                                     target="control_plane-chart"))
            turbo.push(turbo.replace(render_fragments.render_data_plane_chart_fragment(state),
                                     target="data_plane-chart"))
            turbo.push(turbo.replace(render_fragments.render_nav_fragment(state, traceroute_id),
                                     target="nav-ids"))
