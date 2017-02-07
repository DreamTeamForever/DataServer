#!/usr/bin/env python

import server
import multiprocessing

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    server = server.Server("0.0.0.0", 9099)
    try:
	logging.info("Listening...")
	server.start()
    except:
	logging.exception("Starting server error!")
    finally:
	logging.info("Shutting down")
	for process in multiprocessing.active_children():
	    process.terminate()
	    process.join()
    logging.info("All done")