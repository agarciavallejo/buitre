import pytest
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from pathlib import Path

from ...app.entities.opportunity import Opportunity, OpportunityRepository
from ...app.utils.exceptions import ArgumentException
from ...app.services.opportunity.listOpportunitiesService import ListOpportunitiesService

engine = create_engine(os.getenv('TEST_DATABASE_URL'))
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    # run alembic migrations
    alembic_ini_path = Path(__file__).parent.parent.parent.absolute().as_posix() + '/alembic.ini'
    alembic_config = AlembicConfig(alembic_ini_path)
    alembic_config.set_main_option('sqlalchemy.url', os.getenv('TEST_DATABASE_URL'))
    alembic_config.set_main_option('script_location', os.getenv('ALEMBIC_SCRIPT_LOCATION'))
    alembic_upgrade(alembic_config, 'head')
    exit(200)
    yield connection
    connection.close()
    print("connection closed")


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    #transaction.rollback()
    print("session closed & transaction rolled back")


def create_opportunities():
    op1 = Opportunity(name='opo1', user_id=1, latitude=39.5766794, longitude=2.6597445)
    op2 = Opportunity(name='opo2', user_id=1, latitude=39.5822693, longitude=2.6556478)
    op3 = Opportunity(name='opo3', user_id=1, latitude=39.5820563, longitude=2.6457773)
    op4 = Opportunity(name='opo4', user_id=1, latitude=39.5794674, longitude=2.633283)
    op5 = Opportunity(name='opo5', user_id=1, latitude=39.6087669, longitude=2.6884639)

    opportunity_list = [op1, op2, op3, op4, op5]
    return opportunity_list


class FakeOpportunityRepo:
    def __init__(self):
        self.lat = None
        self.lng = None
        self.keywords = None
        self.filters = []

    def initQuery(self):
        self.__init__()

    def centerQuery(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def executeQuery(self):
        return []


@pytest.fixture()
def fakedservice():
    return ListOpportunitiesService(
        opportunityRepository=FakeOpportunityRepo()
    )


@pytest.fixture()
def service():
    return ListOpportunitiesService(
        opportunityRepository=OpportunityRepository()
    )


def test_no_arguments(fakedservice):
    with pytest.raises(ArgumentException):
        fakedservice.call({})


def test_arguments_none(fakedservice):
    args = {
        'lat': None,
        'lng': None,
        'keywords': None,
        'filters': []
    }
    results = fakedservice.call(args)
    assert len(results) == 0


# DB TESTS - fixture binded to ORM :(
def test_latlngsearch(session, service):
    test_database = create_opportunities()
    ## session.query(Opportunity).delete()
    for opportunity in test_database:
        session.add(opportunity)
        session.flush()
        session.commit()

    args = {
        'lat': 5.25,
        'lng': 2.29,
        'keywords': None,
        'filters': []
    }
