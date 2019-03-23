import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from .entities.opportunity import Opportunity

# GraphQL Schema Objects

class OpportunityObject(SQLAlchemyObjectType): 
    class Meta:
        model = Opportunity
        interfaces = (graphene.relay.Node)

class TagObject(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_opportunities = SQLAlchemyConnectionField(OpportunityObject)
    all_tags = SQLAlchemyConnectionField(TagObject)

schema = grapene.Schema(query=Query)