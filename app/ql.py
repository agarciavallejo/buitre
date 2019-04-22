import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from .entities.comment import Comment
from .entities.opportunity import Opportunity
from .entities.opportunitySchedule import OpportunitySchedule
from .entities.picture import Picture
from .entities.tag import Tag
from .entities.user import User

# GraphQL Schema Objects

# COMMENT

class CommentObject(SQLAlchemyObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node, )

# OPPORTUNITY
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

class OpportunityScheduleObject(SQLAlchemyObjectType):
    class Meta:
        model = OpportunitySchedule
        interfaces = (graphene.relay.Node, )

class OpportunityScheduleConnection(graphene.relay.Connection):
    class Meta:
        node = OpportunityScheduleObject

# PICTURE
class PictureObject(SQLAlchemyObjectType):
    class Meta:
        model = Picture
        interfaces = (graphene.relay.Node, )

class PictureConnection(graphene.relay.Connection):
    class Meta:
        node = PictureObject

# TAG
class TagObject(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )

    def resolve_all_tags(self, info):
        query = self.get_query(info)
        return query.all()

class TagConnection(graphene.relay.Connection):
    class Meta:
        node = TagObject

# USER
class UserObject(SQLAlchemyObjectType):
	class Meta:
		model = User
		interfaces = (graphene.relay.Node, )
    

class UserConnection(graphene.relay.Connection):
    class Meta:
        node = UserObject


# GraphQL QUERY definition 
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    comment = graphene.relay.Node.Field(CommentObject)  

    opportunity = graphene.relay.Node.Field(OpportunityObject)
    def resolve_opportunity():
        return 
    all_opportunities = SQLAlchemyConnectionField(OpportunityConnection)

    opportunity_schedule = graphene.relay.Node.Field(OpportunityScheduleObject)

    picture = graphene.relay.Node.Field(PictureObject)
    all_pictures = SQLAlchemyConnectionField(PictureConnection)

    tag = graphene.relay.Node.Field(TagObject)
    all_tags = SQLAlchemyConnectionField(TagConnection)

    user = graphene.relay.Node.Field(UserObject)
    def resolve_user():
        return
    all_users = SQLAlchemyConnectionField(UserConnection)



qlschema = graphene.Schema(query=Query)

