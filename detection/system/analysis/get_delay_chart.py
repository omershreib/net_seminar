from detection.system.analysis.get_data_plane_delay import get_data_plane_delay
import io
import base64
from _datetime import datetime
import matplotlib.dates as mdates
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

#plt.style.use('ggplot')
#plt.style.use('fivethirtyeight')
#plt.style.use('dark_background')

def set_delay_scatter():
    fig = Figure()
    ax = fig.subplots()
    scat = ax.scatter([], [], c='blue')
    ax.set_title('Traceroute Delay Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Delay (ms)')
    ax.grid(True)

    return fig, ax

def get_delay_chart(collection, limit = 25):
    delay_data = []

    mongo_filter = {
        'sensor_id': 2
    }
    sort = list({'timestamp': -1}.items())
    mongo_delay_temp = collection.find(
        filter=mongo_filter,
        sort=sort,
        limit=limit
    )

    for item in mongo_delay_temp:
        pack = (item['timestamp'].strftime("%H:%M:%S"), get_data_plane_delay(item))
        delay_data.append(pack)

    threshold = 150
    #plt.style.use('seaborn-v0_8-dark')
    #plt.style.use('fivethirtyeight')
    plt.style.use('dark_background')

    fig, ax = set_delay_scatter()

    # for t, _ in delay_data:
    #     print(t)

    times = [pd.to_datetime(t) for t, _ in delay_data]
    #times = [datetime.strptime(t, '%H:%M:%S') for t, _ in delay_data]
    #times = [t for t, _ in delay_data]
    delays = [d for _, d in delay_data]

    # label, value
    #return times, delays

    # matplotlib
    plt.scatter(times, delays, color=['blue' if delay < threshold else 'red' for delay in delays])
    plt.plot(times, delays, linestyle='--', color='red', label='Dashed Line')
    #plt.xticks(rotation=45)
    plt.title(f"Delay Timeline (Last {limit} Probes)")

    locator = mdates.MinuteLocator(interval=1)
    formatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)

    plt.tight_layout()


    return fig

    # plt.savefig('delay_chart.png', format='png')
    # plt.close(fig)
    # output.seek(0)
    #
    # return base64.b64encode(output.getbuffer()).decode("ascii")