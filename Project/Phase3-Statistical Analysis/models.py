from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    season_year = Column(String(255))
    champion_team = Column(Integer, ForeignKey("Team.id"))

    team_seasons = relationship("Teams_Seasons", back_populates="season")
    player_stats = relationship("PlayerStats", back_populates="season")


class Teams(Base):
    __tablename__ = "Team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(255))

    seasons = relationship("Teams_Seasons", back_populates="team")
    player_stats = relationship("PlayerStats", back_populates="team")

class Teams_Seasons(Base):
    __tablename__ = "Team_Seasons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    arena = Column(String(255))
    coach = Column(String(255))
    team_id = Column(Integer, ForeignKey("Team.id"))
    season_id = Column(Integer, ForeignKey("seasons.id"))

    team = relationship("Teams", back_populates="seasons")
    season = relationship("Season", back_populates="team_seasons")

class Positions(Base):
    __tablename__ = "Position"
    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(255))

    player_stats = relationship("PlayerStats", back_populates="position")

class Players(Base):
    __tablename__ = "Players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String(255))
    birth_date = Column(Date)
    height = Column(Integer)
    weight = Column(Integer)
    birth_country = Column(String(255))
    college = Column(String(255))
    agility = Column(Float)

    stats = relationship("PlayerStats", back_populates="player")

class PlayerStats(Base):
    __tablename__ = "Player_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("Players.id"))
    team_id = Column(Integer, ForeignKey("Team.id"))
    position_id = Column(Integer, ForeignKey("Position.id"))
    season_id = Column(Integer, ForeignKey("seasons.id"))
    rank = Column(Integer)
    age = Column(Integer)
    experience = Column(Integer)
    innate_ability = Column(Float)
    salary = Column(Float)
    mvp_awards = Column(Integer)
    games = Column(Integer)
    games_started = Column(Integer)
    minutes_played = Column(Integer)
    field_goals_made = Column(Integer)
    field_goals_attempted = Column(Integer)
    field_goals_percent = Column(Float)
    three_point = Column(Integer)
    three_point_attempted = Column(Integer)
    three_point_percent = Column(Float)
    two_point = Column(Integer)
    two_point_attempted = Column(Integer)
    two_point_percent = Column(Float)
    effective_field_goal_percent = Column(Float)
    field_throws_made = Column(Integer)
    field_throws_made_attempted = Column(Integer)
    field_throws_made_percent = Column(Float)
    offensive_rebound = Column(Integer)
    defensive_rebound = Column(Integer)
    total_rebound = Column(Integer)
    assists = Column(Integer)
    steals = Column(Integer)
    blocks = Column(Integer)
    turnovers = Column(Integer)
    personal_fouls = Column(Integer)
    points = Column(Integer)
    triple_double = Column(Integer)
    multi_team_flag = Column(Integer)

    player = relationship("Players", back_populates="stats")
    team = relationship("Teams", back_populates="player_stats")
    season = relationship("Season", back_populates="player_stats")
    position = relationship("Positions", back_populates="player_stats")