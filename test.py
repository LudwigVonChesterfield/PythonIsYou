import game.game as g
import unittest


class BasicComprehensionTest(unittest.TestCase):
    def setUp(self):
        self.game = g.Game()

        self.game.entities = [
            {
                "TEXT": "BABA",
                "IS": set([]),
                "HAS": []
            },
            {
                "TEXT": "KEKE",
                "IS": set([]),
                "HAS": []
            },
            {
                "TEXT": "BABA",
                "IS": set(["RED"]),
                "HAS": []
            }
        ]

    def test_baba_is_you(self):
        r1 = self.game.add_rule("BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_keke_is_you(self):
        r1 = self.game.add_rule("KEKE IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_baba_is_red(self):
        r1 = self.game.add_rule("BABA IS RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("RED", baba["IS"], "BABA IS NOT RED")
        self.assertNotIn("RED", keke["IS"], "KEKE IS RED")
        self.assertIn("RED", red_baba["IS"], "RED BABA IS NOT RED")

    def test_red_baba_is_you(self):
        r1 = self.game.add_rule("RED BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_is_not_you(self):
        r1 = self.game.add_rule("BABA IS NOT YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_baba_is_not_red(self):
        r1 = self.game.add_rule("BABA IS NOT RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("RED", baba["IS"], "BABA IS RED")
        self.assertNotIn("RED", keke["IS"], "KEKE IS RED")
        self.assertNotIn("RED", red_baba["IS"], "RED BABA IS RED")

    def test_not_baba_is_you(self):
        r1 = self.game.add_rule("NOT BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_red_baba_is_you(self):
        r1 = self.game.add_rule("NOT RED BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_keke_is_not_you(self):
        r1 = self.game.add_rule("NOT KEKE IS NOT YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_baba_is_not_not_you(self):
        r1 = self.game.add_rule("BABA IS NOT NOT YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_is_not_not_not_you(self):
        r1 = self.game.add_rule("BABA IS NOT NOT NOT YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_baba_is_not_not_not_not_you(self):
        r1 = self.game.add_rule("BABA IS NOT NOT NOT NOT YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_not_not_baba_is_you(self):
        r1 = self.game.add_rule("NOT NOT BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_not_not_not_baba_is_you(self):
        r1 = self.game.add_rule("NOT NOT NOT BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_not_not_not_baba_is_you(self):
        r1 = self.game.add_rule("NOT NOT NOT NOT BABA IS YOU")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_is_you_and_red(self):
        r1 = self.game.add_rule("BABA IS YOU AND RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

        self.assertIn("RED", baba["IS"], "BABA IS NOT RED")
        self.assertNotIn("RED", keke["IS"], "KEKE IS RED")
        self.assertIn("RED", red_baba["IS"], "RED BABA IS NOT RED")

    def test_baba_is_you_and_not_red(self):
        r1 = self.game.add_rule("BABA IS YOU AND NOT RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

        self.assertNotIn("RED", baba["IS"], "BABA IS RED")
        self.assertNotIn("RED", keke["IS"], "KEKE IS RED")
        self.assertNotIn("RED", red_baba["IS"], "RED BABA IS RED")

    def test_baba_is_you_and_not_red(self):
        r1 = self.game.add_rule("BABA IS YOU AND NOT RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

        self.assertNotIn("RED", baba["IS"], "BABA IS RED")
        self.assertNotIn("RED", keke["IS"], "KEKE IS RED")
        self.assertNotIn("RED", red_baba["IS"], "RED BABA IS RED")

    def test_baba_and_keke_is_red(self):
        r1 = self.game.add_rule("BABA AND KEKE IS RED")

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("RED", baba["IS"], "BABA IS NOT RED")
        self.assertIn("RED", keke["IS"], "KEKE IS NOT RED")
        self.assertIn("RED", red_baba["IS"], "RED BABA IS NOT RED")


if __name__ == "__main__":
    unittest.main()

