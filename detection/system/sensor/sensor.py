from datetime import datetime, timedelta
from detection.detection_tools.traceroute import traceroute_host
from detection.system.database.mongo_inserter import MongoInserter, trace_queue
import threading
import time


class TraceMonitor(threading.Thread):
    def __init__(self, ip_address: str, sensor_ip: str, starttime: datetime, endtime: datetime):
        super().__init__()
        self.ip_address = ip_address
        self.starttime = starttime
        self.endtime = endtime
        self.sensor_ip = sensor_ip
        self._stop_event = threading.Event()
        self._frequency = 15  # in seconds

    def run_traceroute(self):
        """Run traceroute command and return output as string."""
        try:
            return traceroute_host(self.ip_address)
        except Exception as e:
            return f"Error running traceroute: {e}"

    def run(self):
        """Main thread loop: perform traceroute every 1 minute between start and end time."""
        # Wait until starttime
        while datetime.now() < self.starttime and not self._stop_event.is_set():
            time.sleep(1)

        # Perform traceroutes until endtime
        while datetime.now() <= self.endtime and not self._stop_event.is_set():
            print(f"[{datetime.now()}] Running traceroute to {self.ip_address}")
            output = self.run_traceroute()

            pack = (self.sensor_ip, self.ip_address, output)
            trace_queue.put(pack)

            # Sleep for 1 minute
            time.sleep(self._frequency)

    def stop(self):
        """Stop the monitoring thread."""
        self._stop_event.set()


# Example usage:
if __name__ == "__main__":
    ip = "1.1.1.1"
    start = datetime.now() + timedelta(seconds=5)  # start 5 seconds from now
    end = start + timedelta(minutes=3)  # run for 3 minutes

    mongo_inserter = MongoInserter()
    mongo_inserter.connect()

    if not mongo_inserter.is_connect:
        exit(1)

    mongo_inserter.start()

    monitor = TraceMonitor(ip, '192.168.1.246', start, end)
    monitor.start()

    # Optionally stop early after 2 minutes
    # time.sleep(120)
    # monitor.stop()
