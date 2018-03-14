# -*- coding: utf-8 -*-
#
#
# 15.06.2010

import grok
import logging


from z3c.saconfig import EngineFactory, GloballyScopedSession
from z3c.saconfig.interfaces import IEngineCreatedEvent
from zope.app.appsetup.product import getProductConfiguration
from sqlalchemy import Table, MetaData, create_engine

from ukh.schulportal import log


#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


config = getProductConfiguration('database')
DSN = config['dsn']
log(DSN, 'DSN ->')
USER_TABLE = config['user_table']
log(USER_TABLE, 'USER_TABLE ->')
ENR_TABLE = config['enr_table']
log(ENR_TABLE, 'ENR_TABLE ->')
TRG_TABLE = config['trg_table']
log(TRG_TABLE, 'TRG_TABLE ->')


engine_factory = EngineFactory(DSN, echo=False)
scoped_session = GloballyScopedSession()

grok.global_utility(engine_factory, direct=True)
grok.global_utility(scoped_session, direct=True)


engine = engine_factory()
metadata = MetaData(bind=engine)

schema_name = "UKHINTERN"
schema_name2 = "ukhph"
schema_name3 = "educusadat"

users = Table(USER_TABLE.strip(), metadata, schema=schema_name, autoload=True, autoload_with=engine)
einrichtungen = Table(ENR_TABLE.strip(), metadata, schema=schema_name, autoload=True, autoload_with=engine)
traegeruaz = Table(TRG_TABLE.strip(), metadata, schema=schema_name3, autoload=True, autoload_with=engine)
