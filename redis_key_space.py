from redis import Redis

redis_connection = Redis(host="localhost", port=6379)

class RedisNameSpace():
	@staticmethod	
	def valid(redis_key):
		global redis_connection
		if redis_connection.exists(redis_key):
			return False
		for key in redis_connection.scan_iter(f'{redis_key}*'):
			return False
		return True	

	def __init__(self, namespace, parent=None, validate=True):
		if ':' in namespace:
			raise Exception("namespace should not contain ':' as it is used as delimiter.")
		if parent:
			if not isinstance(parent, RedisNameSpace):
				raise Exception("Parent must be a valid RedisNameSpace object.")
			self.key = f'{parent.key}{namespace}:'
		else:
			self.key = f'{namespace}:'
		self.parent = parent
		if validate and not self.valid(self.key):
			raise Exception("namespace already exists in redis.")

	@classmethod
	def load_namespace(cls, ns_key, parent=None):
		if not ns_key.endswith(":"):
			raise Exception("Not a valid namespace key.")
		keys = ns_key.split(':')
		keys.pop()
		if len(keys) == 0:
			return None
		root_key = keys.pop(0)
		root = RedisNameSpace(root_key, parent)
		new_parent = root
		for key in keys:
			ns = RedisNameSpace(key, new_parent)
			new_parent = ns
		return new_parent

	def get_all_keys(self):
		return settings.REDIS.keys(f'{self.key}*')

	def sub(self, key):
		nns = RedisNameSpace(key, self)
		return nns
	
	def get_fq_key(self, key):
		if ':' in key:
			raise Exception("key should not contain ':' as it is used as delimiter.")
		return f'{self.key}{key}'

class RedisKeySpace():
	ROOT = RedisNameSpace("app_name", parent=None, validate=False)
	USERS = RedisNameSpace("users", parent=ROOT, validate=False)

