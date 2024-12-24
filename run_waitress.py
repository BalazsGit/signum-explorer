import os
import multiprocessing
from waitress import serve
from dotenv import load_dotenv
load_dotenv()
from config.wsgi import application  # Adjust this import to point to your WSGI application

# Calculate optimal workers and threads
cpu_count = multiprocessing.cpu_count()
threads = 3 * cpu_count
timeout = 60

# Start waitress server
serve(
	application,
	host="0.0.0.0",
	port=5000,
	threads=threads,
	connection_limit=1000,  # Equivalent to Gunicorn's max_requests
	asyncore_use_poll=True,
	channel_timeout=timeout,
)
