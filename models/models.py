from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'Profile'
    Id_User = Column(Integer, primary_key=True)
    User_mail = Column(String(100), unique=True)
    Name = Column(String(100))
    Lastname = Column(String(100))
    Description = Column(String(255))
    Id_preferences = Column(Integer, ForeignKey("Preferences.Id_preferences"))
    Id_type = Column(Integer, ForeignKey("Types.Id_type"))
    Status_account = Column(Integer, CheckConstraint("Status_account IN (0, 1)"))

class Followers(Base):
    __tablename__ = 'Followers'
    Id_Follows = Column(Integer, primary_key=True, autoincrement=True)
    Id_Follower = Column(Integer, ForeignKey("Profile.Id_User"))
    Id_Following = Column(Integer, ForeignKey("Profile.Id_User"))
    Status = Column(Integer, CheckConstraint("Status IN (0, 1)"))
