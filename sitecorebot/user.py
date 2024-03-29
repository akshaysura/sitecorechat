import random
from slack_bolt import App
from expiring_dict import ExpiringDict

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
user_nicolemontero = "U01U3AMHVC0"

bot_admins = [user_cassidydotdk, user_akshaysura, user_sitecorejunkie, user_jammykam, user_michaelwest, user_longhorntaco, user_marekmusielak, user_tamastarnok]
community_coordinators = [user_tamasvarga, user_nicolemontero]

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
    def is_community_coordinator(self) -> bool:
        return self.id in community_coordinators
    
    @property
    def real_name(self) -> str:
        return self._userinfo["real_name"]
    
    @property
    def email_address(self) -> str:
        if self._userinfo["profile"] and self._userinfo["profile"]["email"]:
            return self._userinfo["profile"]["email"]
        else:
            return "<No Profile Information>"
        
    def send_im_message(self, text=None, blocks=None):
        self._app.client.chat_postMessage(channel=self.id, text=text, blocks=blocks)

### CACHING ###
cache_users = ExpiringDict()

def is_bot_admin_user(user_id) -> bool:
    return user_id in bot_admins

def is_community_coordinator(user_id) -> bool:
    return user_id in community_coordinators

def get_user(app, user_id) -> User:
    if user_id in cache_users:
        return cache_users[user_id]
    else:
        try:
            userinfo = app.client.users_info(user=user_id)["user"]
            user = User(app, userinfo)
            cache_users.ttl(user_id, user, random.randint(3600, 7200))
            return user
        except:
            print(f"ERR: User Not Found! ({user_id})")
            return None

def get_user_by_email(app: App, email) -> User:
        try:
            userinfo_request = app.client.users_lookupByEmail(email=email)
            return get_user(app, userinfo_request["user"]["id"])
        except:
            return None

print(f"User Manager Online. Bot Admins:", bot_admins)
