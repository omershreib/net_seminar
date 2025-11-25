from detection.dashboard.render_fragments import render_fragments
from detection.dashboard.dashboard_tools import compute_state
import time

def updater_loop(app, turbo):
    """Background updater that pushes Turbo replaces to the client every 3 minutes."""
    with app.app_context():
        while True:
            time.sleep(60)  # 3 minutes
            # We refresh based on the currently viewed UUID; if none, skip
            # For a single-page per UUID, you can derive it from request args during initial render.
            # Here we choose to refresh the last requested UUID if present; otherwise skip.
            # In multi-client setups, consider storing per-client UUID in session or pushing channels.
            traceroute_id = getattr(updater_loop, "last_uuid", None)
            if not traceroute_id:
                continue
            state = compute_state(traceroute_id)
            if not state:
                continue

            turbo.push(turbo.replace(render_fragments.render_data_plane_fragment(state), target="data-plane"))
            turbo.push(turbo.replace(render_fragments.render_delay_chart_fragment(state), target="delay-chart"))
            turbo.push(turbo.replace(render_fragments.render_control_plane_chart_fragment(state),
                                     target="control_plane-chart"))
            turbo.push(
                turbo.replace(render_fragments.render_data_plane_chart_fragment(state), target="data_plane-chart"))
            turbo.push(turbo.replace(render_fragments.render_nav_fragment(state, traceroute_id), target="nav-ids"))