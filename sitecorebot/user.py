# bot admin users
user_cassidydotdk = "U0D8XHJSH"
user_akshaysura = "U09SJ4FGW"
user_sitecorejunkie = "U09SJGX5X"
user_jammykam = "U0A1FKM24"
user_michaelwest = "U09SK9G1F"
user_longhorntaco = "U0C29A1MG"
user_marekmusielak = "U09UVE83Y"
user_tamastarnok = "U3H1FSTU2"

# mvp program coordinators
user_tamasvarga = "U0BAH3W05"
user_nicolemontero = ""

bot_admins = [user_cassidydotdk, user_akshaysura, user_sitecorejunkie, user_jammykam, user_michaelwest, user_longhorntaco, user_marekmusielak, user_tamastarnok]
mvp_coordinators = [user_tamasvarga, user_nicolemontero]

class User:
    def __init__(self, app, userinfo):
        self._app = app
        self._userinfo = userinfo

    @property
    def id(self) -> str:
        return self._userinfo["id"]
    
    @property
    def name(self) -> str:
        return self._userinfo["name"]
    
    # having this flag does not automatically imply a bot admin
    @property
    def is_admin(self) -> bool:
        return self._userinfo["is_admin"]
    
    @property
    def is_bot_admin(self) -> bool:
        return self.id in bot_admins
    
    @property
    def real_name(self) -> str:
        return self._userinfo["real_name"]

### CACHING ###

cache_users = {}

def get_user(app, user_id) -> User:
    if user_id in cache_users:
        return cache_users[user_id]
    else:
        try:
            userinfo = app.client.users_info(user=user_id)["user"]
            user = User(app, userinfo)
            cache_users[user_id] = user
            return user
        except:
            print(f"ERR: User Not Found! ({user_id})")
            return None

def get_user_by_email(app, email) -> User:
        try:
            userinfo_request = app.client.users_lookupByEmail(email=email)
            return get_user(app, userinfo_request["user"]["id"])
        except:
            return None
