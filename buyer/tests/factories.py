import factory
import factory.fuzzy

from directory_validators.constants import choices

from buyer.models import Buyer


SECTORS = [i[0] for i in choices.COMPANY_CLASSIFICATIONS]


class BuyerFactory(factory.django.DjangoModelFactory):

    name = factory.fuzzy.FuzzyText(length=12)
    email = factory.LazyAttribute(
        lambda buyer: '%s@example.com' % buyer.name)
    sector = factory.fuzzy.FuzzyChoice(SECTORS)
    company_name = factory.fuzzy.FuzzyText(length=12)
    country = factory.fuzzy.FuzzyChoice(
        ['Germany', 'China', 'Japan', 'Neverland', 'Roman Empire'])

    class Meta:
        model = Buyer
