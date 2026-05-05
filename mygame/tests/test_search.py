from evennia.utils.test_resources import EvenniaTest
from evennia import create_object

class TestPluralSearch(EvenniaTest):

    def setUp(self):
        super().setUp()

        for obj in self.char1.location.contents:
            if obj is not self.char1:
                obj.delete()

        self.rock1 = create_object("evennia.objects.objects.DefaultObject",
                                   key="rock",
                                   location=self.char1.location)

        self.rock2 = create_object("evennia.objects.objects.DefaultObject",
                                   key="rock",
                                   location=self.char1.location)

        self.rock3 = create_object("evennia.objects.objects.DefaultObject",
                                   key="rock",
                                   location=self.char1.location)

    def test_plural_behavior(self):
        singular = self.char1.search("rock", quiet=True)
        plural = self.char1.search("rocks", quiet=True)

        self.assertEqual(len(singular), 3)
        self.assertEqual(len(plural), 0)