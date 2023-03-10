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

class CreateOrder(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        total_in_cents = graphene.Int()
        customer = graphene.ID()

    order = graphene.Field(OrderType)

    def mutate(root, info, description, total_in_cents, customer):
# option 1
#      order = Order(description=description, total_in_cents=total_in_cents, customer_id=customer)
#      order = Order(description=description, total_in_cents=total_in_cents, customer_id=customer)
# option 2 (next 2 lines replaced by above)
        cid = Customer.objects.get(pk=customer)
        order = Order(description=description, total_in_cents=total_in_cents, customer=cid)
        order.save()
        return CreateOrder(order=order)


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
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)

