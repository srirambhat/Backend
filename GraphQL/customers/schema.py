import graphene
from graphene_django import DjangoObjectType
# import time
from customers.models import Customer, Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        industry = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(root, info, name, industry):
#        time.sleep(5)
        customer = Customer(name=name, industry=industry)
        customer.save()
        return CreateCustomer(customer=customer)

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    customer_by_name = graphene.List(CustomerType, name=graphene.String(required=True))
    orders = graphene.List(OrderType)

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_customer_by_name(root, info, name):
        try:
            return Customer.objects.filter(name=name)
        except Customer.DoesNotExist:
            return None

    def resolve_orders(root, info):
        return Order.objects.selected_related('customer').all()

class Mutations(graphene.ObjectType):
    createCustomer = CreateCustomer.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)

