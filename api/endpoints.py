from enum import Enum

class Endpoints(Enum):
    """Auth"""
    POST_LOGIN_PROVIDER = "/login/{provider}"
    POST_LOGOUT = "/logout"
    POST_GUEST_LOGIN = "/guest/login"

    """Banners"""
    GET_BANNERS = "/banners"
    GET_BANNERS_BANNER = "/banners/{banner}"

    """Coin packages"""
    GET_COIN_PACKAGES = "/coin-packages"
    POST_COIN_PACKAGES = "/coin-packages"

    """Collections"""
    GET_COLLECTIONS = "/collections"
    GET_COLLECTIONS_COLLECTION = "/collections/{collection}"
    GET_COLLECTIONS_COLLECTION_CONTENTS = "/collections/{collection}/contents"

    """Contents"""
    GET_NEXT_TITLE = "/next-title"
    #TODO: GET_CONTENT нет в swagger
    GET_CONTENTS = "/contents/"
    GET_CONTENTS_CONTENT = "/contents/{content}"
    GET_CONTENTS_CONTENT_EPISODES = "/contents/{content}/episodes"

    """Genres"""
    GET_GENRES = "/genres"
    GET_GENRES_GENRE_ID_CONTENTS = "/genres/{genre_Id}/contents"

    """Episodes"""
    POST_EPISODES_EPISODE_LIKE = "/episodes/{episode}/like"
    DELETE_EPISODES_EPISODE_LIKE = "/episodes/{episode}/like"
    POST_EPISODES_EPISODE_PURCHASE = "/episodes/{episode}/purchase"

    """Favorites"""
    GET_FAVORITES_CONTENTS = "/favorites/contents_models"
    POST_FAVORITES_CONTENTS_CONTENT = "/favorites/contents_models/{content}"
    DELETE_FAVORITES_CONTENTS_CONTENT = "/favorites/contents_models/{content}"

    """History"""
    GET_HISTORY = "/history"
    POST_HISTORY_EPISODE = "/history/{episode}"

    """Languages"""
    GET_LANGUAGES = "/languages"

    """Pushes"""
    POST_PUSHES_TOKEN = "/pushes/token"
    DELETE_PUSHES_TOKEN = "/pushes/token"
    POST_PUSHES_PUSHMESSAGE_SET_READ = "/pushes/{pushMessage}/set-read"

    """Promo Codes"""
    POST_PROMO_CODES = "/promo-codes"

    """Rewards"""
    GET_REWARDS = "/rewards"
    POST_REWARDS_SLUG = "/rewards/{slug}"

    """Search"""
    GET_SEARCH = "/search_models"
    GET_SEARCH_HINTS = "/search/hints"

    """Subscriptions"""
    GET_SUBSCRIPTIONS = "/subscriptions"
    POST_SUBSCRIPTIONS = "/subscriptions"
    POST_SUBSCRIPTIONS_SUBSCRIPTION_CANCEL = "/subscriptions/{subscription}/cancel"
    POST_SUBSCRIPTIONS_SUBSCRIPTION_RESUME = "/subscriptions/{subscription}/resume"

    """User"""
    GET_USER = "/user"
    DELETE_USER = "/user"
    GET_USER_SUBSCRIPTIONS = "/user/subscriptions"
    POST_USER_LANGUAGE = "user/language"
    GET_USER_COIN_TRANSACTIONS = "user/coin-transactions"
    GET_USER_PAYMENT_HISTORY = "user/payment-history"
    GET_USER_COIN_BALANCE = "user/coin-balance"

    """Purchases GooglePlay"""
    POST_PURCHASES_GOOGLE_PLAY = "/purchases/google-play"

    """Client App"""
    GET_CLIENT_APP_ACCESS = "/client-app/access"