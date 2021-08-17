import factory
from auth_service_api.models import User


class UserFactory(factory.Factory):

    full_name = factory.Sequence(lambda n: "user%d" % n)
    bin = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User
