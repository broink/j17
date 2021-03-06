from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product_association = Table('product_association', pre_meta,
    Column('cafe_id', INTEGER),
    Column('product_id', INTEGER),
)

product_association_table = Table('product_association_table', post_meta,
    Column('cafe_id', Integer),
    Column('product_id', Integer),
)

cafe = Table('cafe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=128)),
    Column('products', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product_association'].drop()
    post_meta.tables['product_association_table'].create()
    pre_meta.tables['cafe'].columns['products'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product_association'].create()
    post_meta.tables['product_association_table'].drop()
    pre_meta.tables['cafe'].columns['products'].create()
