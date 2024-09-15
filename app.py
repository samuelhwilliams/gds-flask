import random
import uuid
from cgi import print_arguments

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy_lite import SQLAlchemy
from govuk_flask_admin import GovukFrontendV5_6Theme, GovukFlaskAdmin
from jinja2 import PackageLoader, ChoiceLoader, PrefixLoader
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    age: Mapped[int]
    job: Mapped[str]

app = Flask(__name__)
app.jinja_options = {
    "loader": ChoiceLoader(
        [
            PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
            PackageLoader("govuk_flask_admin"),
        ]
    )
}

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///default.sqlite"}

admin = Admin(app, theme=GovukFrontendV5_6Theme())
govuk_flask_admin = GovukFlaskAdmin(app)

db = SQLAlchemy(app)
with app.app_context():
    Base.metadata.create_all(db.engine)

    db.session.add(User(email=str(uuid.uuid4()), name=str(uuid.uuid4()), age=random.randint(18, 100), job='blah blah'))
    db.session.commit()

    admin.add_view(ModelView(User, db.session))
