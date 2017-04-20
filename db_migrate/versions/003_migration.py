from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('added_by', INTEGER),
    Column('timestamp_added', DATETIME),
    Column('name', VARCHAR(length=128)),
    Column('descr', TEXT),
    Column('price', INTEGER),
    Column('picture', TEXT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['added_by'].drop()
    pre_meta.tables['product'].columns['picture'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['added_by'].create()
    pre_meta.tables['product'].columns['picture'].create()
