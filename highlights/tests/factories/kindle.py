from highlights import enums
import factory
from faker import Faker

fake = Faker()


class KindleHighlight(factory.Factory):
    class Meta:
        model = enums.KindleHighlight

    id = factory.Sequence(lambda n: n)
    highlight = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=2))


class KindleCsvData(factory.Factory):
    class Meta:
        model = enums.KindleCsvData

    title: str = "Fake title"
    author: str = fake.name()
    highlights = factory.List(
        [factory.SubFactory(KindleHighlight) for _ in range(5)]
    )
