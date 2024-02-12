from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Game(db.Model, SerializerMixin):
    # __tablename__ = 'games'

    # serialize_rules = ('-players.game',)

    id = db.Column(db.Integer, primary_key=True)
    visitor = db.Column(db.String)
    home = db.Column(db.String)
    location = db.Column(db.String)
    temperature = db.Column(db.Integer)
    wind_direction = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)
    precipitation = db.Column(db.String)
    cloud_or_sun = db.Column(db.String)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # at_bats = db.relationship('AtBat', back_populates="game")
    at_bats = db.relationship('AtBat', backref=db.backref('game'))

    def __repr__(self):
        return f'<{self.visitor} at {self.home} {self.date}>'

class FinalBet(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    category_value = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    prop = db.Column(db.String)
    line = db.Column(db.Integer)
    algorithm = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

    def __repr__(self):
        return f'<{self.category} {self.category_value} ({self.date}): {self.name} {self.line} {self.prop}>'


class Pitcher(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    arm = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    at_bats = db.relationship('AtBat', backref=db.backref('pitcher'))

    

    def __repr__(self):
        return f'<{self.name}>'


class Hitter(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bat = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # at_bats = db.relationship('AtBat', back_populates='hitter')
    at_bats = db.relationship('AtBat', backref=db.backref('hitter'))

    

    def __repr__(self):
        return f'<{self.name}>'


class AtBat(db.Model, SerializerMixin):
    # __tablename__ = 'at_bat'

    id = db.Column(db.Integer, primary_key=True)
    inning = db.Column(db.Integer)
    pitches = db.Column(db.String)
    balls = db.Column(db.String)
    strikes = db.Column(db.String)
    result = db.Column(db.String)
    strength = db.Column(db.String)
    location = db.Column(db.String)
    rbi = db.Column(db.Integer)
    score = db.Column(db.Integer)
    sb = db.Column(db.Integer)
    sb_att = db.Column(db.Integer)
    team = db.Column(db.String)

    hitter_id = db.Column('hitter_id',db.Integer, db.ForeignKey('hitter.id'))
    pitcher_id = db.Column('pitcher_id',db.Integer, db.ForeignKey('pitcher.id'))
    game_id = db.Column('game_id',db.Integer, db.ForeignKey('game.id'))


    def __repr__(self):
        return f"<{self.pitcher.name} vs {self.hitter.name} on {self.game.date}>"

# class Team(db.Model, SerializerMixin):
#     __tablename__ = 'teams'

#     serialize_rules = ('-.user',)

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
    
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     players = db.relationship('Players', backref='team')
#     games = db.relationship('Games', backref='team')
