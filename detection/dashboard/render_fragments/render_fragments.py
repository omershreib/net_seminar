from flask import render_template_string

def render_data_plane_fragment(state):
    return render_template_string(
        """
            <div class="container mx-auto p-2" style="color: white;">
      <h6 name="uuid" style="text-align: justify;">UUID: {{ data_plane._id }}</h6>
      <h6 style="text-align: justify;">datetime:    {{ data_plane.timestamp }}</h6>
      <h6 style="text-align: justify;">sensorId:    {{ data_plane.sensor_id }}</h6>
      <h6 style="text-align: justify;">destination: {{ data_plane.destination_ip }}</h6>
    </div>

    <div class="container">
      <div class="d-grid gap-2 d-md-flex justify-content-md-end" style="margin-bottom: 2%;">
          <a name="btn_previous" onclick="performPost()" class="btn btn-outline-light" style="margin-right: 1%;" type="submit" href="{{ url_for('dashboard', uuid=prev_id) }}">previous</a>
          <a name="btn_next"  onclick="performPost()" class="btn btn-outline-light" type="submit" href="{{ url_for('dashboard', uuid=next_id) }}">next</a>
      </div>
      <div class="table-responsive">
      <table id="data_plane" class="table table-dark table-striped table-hover table-bordered">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col">IP</th>
              <th scope="col">ASN</th>
            </tr>
          </thead>
          <tbody>
            {% for hop in data_plane.hops %}
              <tr>
                <td>{{ hop.hop_num }}</td>
                  {% if hop.delays[0] %}
                <td>{{ hop.delays[0] | round | int if hop.delays[0] else '*' }}ms</td>
                  {% else %}
                <td> * </td>
                  {% endif %}

                  {% if hop.delays[1] %}
                <td>{{ hop.delays[1] | round | int if hop.delays[0] else '*' }}ms</td>
                  {% else %}
                <td> * </td>
                  {% endif %}
                  {% if hop.delays[2] %}
                <td>{{ hop.delays[2] | round | int if hop.delays[0] else '*' }}ms</td>
                  {% else %}
                <td> * </td>
                  {% endif %}

                <td>{{ hop.hop_ip }}</td>
                <td>{{ hop.asn }}</td>
              </tr>
            {% endfor %}
          </tbody>
      </table>
      </div>
    </div>
        """,
        data_plane=state["data_plane"])


def render_delay_chart_fragment(state):
    return render_template_string(
        """
        <div id="delay-chart">
          <h2>Delay chart</h2>
          <img src="{{ url }}?ts={{ ts }}" alt="Delay chart">
        </div>
        """,
        url=state["delay_chart_url"], ts=state["ts"]
    )


def render_control_plane_chart_fragment(state):
    return render_template_string(
        """
        <div id="control_plane-chart">
          <h2>Control plane chart</h2>
          <img src="{{ url }}?ts={{ ts }}" alt="Control plane chart">
        </div>
        """,
        url=state["control_plane_chart_url"], ts=state["ts"]
    )


def render_data_plane_chart_fragment(state):
    return render_template_string(
        """
        <div id="data_plane-chart">
          <h2>Data plane chart</h2>
          <img src="{{ url }}?ts={{ ts }}" alt="Data plane chart">
        </div>
        """,
        url=state["data_plane_chart_url"], ts=state["ts"]
    )


def render_nav_fragment(state, traceroute_id):
    return render_template_string(
        """
        <div id="nav-ids">
          <a href="{{ url_for('dashboard', uuid=prev_id) }}">Previous</a> |
          <a href="{{ url_for('dashboard', uuid=next_id) }}">Next</a> |
          <span>Current: {{ curr }}</span>
        </div>
        """,
        prev_id=state["prev_id"], next_id=state["next_id"], curr=traceroute_id
    )
