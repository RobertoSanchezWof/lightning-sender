import json
from datetime import datetime, timedelta

data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-44.9836,"lon":-23.2752}'
data = json.loads(data)
valueTime = [pulse["time"] for pulse in data["Pulses"]] # Obtener los tiempos de cada pulso

date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
unix_timestamps = []
for x in valueTime:
    ts_truncated = x[:-4] + 'Z'
    unix_timestamp = datetime.strptime(ts_truncated, date_format).timestamp()
    unix_timestamps.append(unix_timestamp)

# Encuentra el menor y el mayor de los timestamps
min_timestamp = min(unix_timestamps)
max_timestamp = max(unix_timestamps)

# Calcula la duración entre el menor y el mayor de los timestamps
durationSeconds = max_timestamp - min_timestamp
duration = timedelta(seconds=durationSeconds)
print("Duración entre el menor y el mayor (segundos): ", duration)