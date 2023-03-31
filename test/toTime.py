from datetime import datetime
import numpy as np

timestamps = [
    '2023-03-08T16:25:50.766793518Z',
    '2023-03-08T16:25:50.696567000Z',
    '2023-03-08T16:25:50.651452872Z'
]

# Define el formato de fecha y hora
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

# Trunca la parte de microsegundos a 6 dígitos
timestamps_truncated = [ts[:-4] + 'Z' for ts in timestamps]

# Convierte las fechas truncadas a objetos datetime y luego a timestamps
unix_timestamps = [datetime.strptime(ts, date_format).timestamp() for ts in timestamps_truncated]

min_timestamp = min(unix_timestamps)
max_timestamp = max(unix_timestamps)

duration = max_timestamp - min_timestamp

# Imprime los resultados
print("Timestamps en formato Unix: ", unix_timestamps)
print("Duraciones (segundos): ", duration)
