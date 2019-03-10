from gi.repository import Gio

# signature type code
TYPE_FD = "h"

def is_supported(conn):
	"""
	Check if the message bus supports passing of Unix file descriptors.
	"""
	return conn.get_capabilities() & Gio.DBusCapabilityFlags.UNIX_FD_PASSING


def extract(params, signature, fd_list):
	"""
	Extract any file descriptors from a UnixFDList (e.g. after
	receiving from D-Bus) to a parameter list.
	Receiver must call os.dup on any fd it decides to keep/use.
	"""
	if not fd_list:
		return params
	fd_list = (fd
		   for fd
		   in fd_list.peek_fds())
	return [next(fd_list)
		if arg == TYPE_FD
		else val
		for val, arg
		in zip(params, signature)]


def make_fd_list(params, signature):
	"""
	Embed any unix file descriptors in a parameter list into a
	UnixFDList (for D-Bus-dispatch).
	"""
	if not any(arg
		   for arg in signature
		   if arg == TYPE_FD):
		return None
	fd_list = Gio.UnixFDList()
	for fd in [param
		   for param, arg
		   in zip(params, signature)
		   if arg == TYPE_FD]:
		fd_list.append(fd)
	return fd_list
