# redis-namespace
Usage::
 0. Namespaces are identified by strings ending with ':'. We can have nested namespaces eg: app_name:users:
 
 1. To get fully-qualified redis-key inside a namespace use get_fq_key method:
    
    eg. To store data({"name": "bazinga"}) for user with user_id = "7e3e10c7".
    redis_key = RedisKeySpace.USERS.get_fq_key(user_id)
    redis_connection.set(redis_key, user_data)
    
    Always store data on key inside namespace ie keys not ending with ':'. 
    Don't store data in keys ending with ':'.(Except in some cases when we want to store meta model level metadata at such keys.) 
    
 2. It's good to have one top level namespace for entire app especially when a centralized redis cluster is used by many 
    different apps. All other namespaces are nested within this top level namespace.
    
   eg: RedisKeySpace.ROOT refers to top level namespace for entire app.
     
 3. Define all preknown namespaces(eg. model level namespaces) at one place. 
    RedisKeySpace.USERS is namespace for holding users data. It is nested inside RedisKeySpace.ROOT(app_name:) namespace. 
 
 4. To create a nested namespace inside some namespace object use *sub* method.
    Constructor of class RedisNameSpace raises error if same namespace object is already existing jusst to avoid accidental
    overide of data. You can suppress the error by sending validate=False in constructor. 
     
 5. Use load_namespace to get RedisNameSpace object from namespace key. Whole namespace ancestor chain can be accessed by 
 calling parent on namespace object. 
 
 6. get_all_keys method for getting all keys inside a namespace.
