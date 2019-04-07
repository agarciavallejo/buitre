import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from .entities.opportunity import Opportunity
from .entities.tag import Tag
from .entities.user import User

# GraphQL Schema Objects

class OpportunityObject(SQLAlchemyObjectType): 
    class Meta:
        model = Opportunity
        interfaces = (graphene.relay.Node, )

    def resolve_all_oportunities(self, info):
        query = self.get_query(info)
        return query.all()

class OpportunityConnection(graphene.relay.Connection):
    class Meta:
        node = OpportunityObject

class TagObject(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )

class UserObject(SQLAlchemyObjectType):
	class Meta:
		model = User
		interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    hello = graphene.String(argument=graphene.String(default_value="stranger"))
    
    def resolve_hello(self, info, argument):
        return 'Hola '+argument

    opportunity = graphene.relay.Node.Field(OpportunityObject)

    def resolve_opportunity():
        return 

    all_opportunities = SQLAlchemyConnectionField(OpportunityConnection)



qlschema = graphene.Schema(query=Query)

