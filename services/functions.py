from models.models import Followers, Profile
from conections.mysql import conection_userprofile

def get_following(user_id):
    session = conection_userprofile()

    profile = session.query(Profile).filter_by(Id_User=user_id, Status_account=1).first()
    if not profile:
        session.close()
        return {"error": "Active profile not found"}, 404

    following = (
        session.query(Profile)
        .join(Followers, Profile.Id_User == Followers.Id_Following)
        .filter(Followers.Id_Follower == user_id, Followers.Status == 1)
        .all()
    )

    result = [
        {
            "Id_User": p.Id_User,
            "User_mail": p.User_mail,
            "Name": p.Name,
            "Lastname": p.Lastname
        } for p in following
    ]

    session.close()
    return {"following": result}, 200
