from evennia.utils.test_resources import EvenniaTest
from evennia.utils.create import create_object


class TestPluralSearch(EvenniaTest):

    def test_plural_behavior(self):
        pencil1 = create_object("evennia.objects.objects.DefaultObject",
                                key="pencil",
                                location=self.char1.location)
        pencil2 = create_object("evennia.objects.objects.DefaultObject",
                                key="pencil",
                                location=self.char1.location)

        # check what aliases were actually registered
        print(list(pencil1.aliases.all()))
        print(list(pencil2.aliases.all()))

        plural = self.char1.search("pencils", quiet=True, stacked=10)
        self.assertEqual(len(plural), 2)