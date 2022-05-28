import graphene
import datetime
from django.db.models import Sum
from django.utils import timezone
from graphql_auth import mutations
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import MyUser, Clock

class UserType(DjangoObjectType):
    class Meta:
        model = MyUser
        # allow query of only these fields
        fields = ("username","email","id")

class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        # allow query of only these fields
        fields = ("id", "user", "clockedIn", "clockedOut")


class Query(graphene.ObjectType):

    currentClock = graphene.Field(
        ClockType
    )

    @login_required
    # allow authenticated users only
    def resolve_currentClock(root, info):
        user = MyUser.objects.get(username=info.context.user.username)
        user_id = user.id
        if user.clock_active:
            # user has active clock
            return Clock.objects.filter(user_id = user_id).last()
        else:
            return None

    clockedHours = graphene.JSONString()

    @login_required
    def resolve_clockedHours(root, info ):
        user = MyUser.objects.get(username = info.context.user.username)
        user_id = user.id
        current_date = datetime.date.today()
        result = {
            'today' : Clock.objects.filter(user_id = user_id).filter(current_date=datetime.date.today()).values_list('totalHours').aggregate(Sum('totalHours'))['totalHours__sum'],
            'currentWeek' : Clock.objects.filter(user_id = user_id).filter(current_date__week=current_date.isocalendar()[1]).values_list('totalHours').aggregate(Sum('totalHours'))['totalHours__sum'],
            'currentMonth' : Clock.objects.filter(user_id = user_id).filter(current_date__month= current_date.month).values_list('totalHours').aggregate(Sum('totalHours'))['totalHours__sum'],
        }
        return result

    me = graphene.Field(
        UserType
    )
    @login_required
    def resolve_me(root,info):
        user =  MyUser.objects.get(username=info.context.user.username)
        return  user

class ClockIn(graphene.Mutation):
    
    # subfield that will return on mutation
    clock = graphene.Field(
        ClockType
    )

    @classmethod
    def mutate(cls,root,info):
        if info.context.user.is_authenticated:
            user = MyUser.objects.get(username=info.context.user.username)
            if not user.clock_active:
                # if User is not already active
                clock = Clock()
                clock.current_date = datetime.date.today()
                clock.clockedIn = timezone.now()
                clock.clockedOut = None
                clock.totalHours = 0
                clock.user = user
                user.clock_active = True
                clock.save()
                user.save()
                return ClockIn(clock = clock)
            else:
                # if active then, can raise error message as well
                return Exception('User Already ClockedIn')
        else:
            raise Exception("Authentication credentials were not provided")

class ClockOut(graphene.Mutation):

    clock = graphene.Field(
        ClockType
    )

    @classmethod
    def mutate(cls,root,info):
        if info.context.user.is_authenticated:
            user = MyUser.objects.get(username=info.context.user.username)
            if user.clock_active:
                # if User is not already active
                clock = Clock.objects.filter(user_id = user.id).last()
                query_date =datetime.date.today()
                clocked_date = clock.current_date
                print(query_date, clocked_date)
                if clocked_date == query_date:
                    clock.clockedOut = timezone.now()
                    clock.totalHours = (clock.clockedOut - clock.clockedIn).seconds//3600
                    user.clock_active = False
                    user.save()
                    clock.save()
                    return ClockOut(clock = clock)
                else:
                    # different clocking dates
                    # can implement logic where
                    # clock out within 8 hour window?
                    # yes? -> calculate total hours
                    # no? -> notify to resolve irregularity
                    # Deactivate existing Clock 
                    user.clock_active = False
                    user.save()
                    return Exception('Irregularity in SignIn/SignOut. Please Sign In Again and Raise a Resolve Request on the HR Portal.')
            else:
                return Exception('User not Clocked In')
        else:
            raise Exception("Authentication credentials were not provided")

class Mutation(graphene.ObjectType):
    createUser = mutations.Register.Field('createUser')
    verify_account = mutations.VerifyAccount.Field()
    obtainToken = mutations.ObtainJSONWebToken.Field()
    clockIn = ClockIn.Field()
    clockOut = ClockOut .Field()
