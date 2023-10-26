# bot admin users
user_cassidydotdk = "U0D8XHJSH"
user_akshaysura = "U09SJ4FGW"
user_sitecorejunkie = "U09SJGX5X"
user_jammykam = "U0A1FKM24"
user_michaelwest = "U09SK9G1F"
user_longhorntaco = "U0C29A1MG"

# mvp program coordinators
user_tamasvarga = "U0BAH3W05"

# No special priveleges implemented for admins yet
bot_admins = [user_cassidydotdk, user_akshaysura, user_sitecorejunkie, user_jammykam, user_michaelwest, user_longhorntaco]

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
            return None
