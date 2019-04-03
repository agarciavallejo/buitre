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

# class CreateUser(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID()
#         name = graphene.String(required=True)
#         email = graphene.String(required=True)
#         password = graphene.String(required=True)
#         latitude = graphene.Float()
#         longitude = graphene.Float()
#         radius = graphene.Int()
#         is_valid = graphene.Boolean()
#         score = graphene.Int()

#     def mutate(self, info, name, email, password):
#         user = User(name, email, password)
#         ok=True
#         return CreateUser(user = user, ok=ok)
class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    hello = graphene.String(argument=graphene.String(default_value="stranger"))
    
    def resolve_hello(self, info, argument):
        return 'Hola '+argument

    opportunity = graphene.relay.Node.Field(OpportunityObject)
    # tag = graphene.relay.Node.Field(TagObject)
    # user = graphene.relay.Node.Field(UserObject)

    def resolve_opportunity():
        return 

    all_opportunities = SQLAlchemyConnectionField(OpportunityConnection)
    #all_tags = SQLAlchemyConnectionField(TagObject)
    #all_users = SQLAlchemyConnectionField(UserObject)

    # def resolve_all_opportunities(self, info, **kwargs):
    #     query = OpportunityObject.get_query(info)
    #     return query.all()


qlschema = graphene.Schema(query=Query)