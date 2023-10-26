import sqlalchemy as sql
import app

class User(app.base):
    __tablename__ = 'users'

    id = sql.Column(sql.BigInteger, primary_key=True, autoincrement=True)

    email = sql.Column(sql.String(255), unique=True, nullable=False)
    phone = sql.Column(sql.String(15), unique=True)

    username = sql.Column(sql.String(255), unique=True, nullable=False)
    first_name = sql.Column(sql.String(63))
    last_name = sql.Column(sql.String(63))
    middle_name = sql.Column(sql.String(63))

    hashed_password = sql.Column(sql.String(255), nullable=False)
    permissions = sql.Column(sql.SmallInteger(), nullable=False)

    is_active = sql.Column(sql.SmallInteger(), nullable=False)
    is_confirmed = sql.Column(sql.Boolean(), nullable=False)
    is_deleted = sql.Column(sql.Boolean(), nullable=False)
    is_banned = sql.Column(sql.Boolean(), nullable=False)

    created_at = sql.Column(sql.DateTime, server_default=sql.sql.func.now())
    updated_at = sql.Column(sql.DateTime, server_default=sql.sql.func.now(), onupdate=sql.sql.func.now())
