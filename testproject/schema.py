import graphene

from timeclock.schema import Query as timeclock_query
from timeclock.schema import Mutation as timeclock_mutations 

class Query(timeclock_query):
     pass

class Mutation(timeclock_mutations):
     pass

schema = graphene.Schema(query = Query, mutation = Mutation)