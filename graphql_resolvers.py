from ariadne import QueryType
from services.functions import get_following

query = QueryType()

@query.field("following")
def resolve_following(_, info):
    user_id = info.context.get("user_id")
    if not user_id:
        raise Exception("Not authenticated")
    response, code = get_following(user_id)
    if code != 200:
        raise Exception(response.get("error", "Unknown error"))
    if isinstance(response, dict) and "following" in response: #If the response is a Dict we returned it with type List
        return response["following"]
    return response 
