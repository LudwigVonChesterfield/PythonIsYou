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
        r1 = self.game.get_rule("BABA IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_is_not_you(self):
        r1 = self.game.get_rule("BABA IS NOT YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("NOT YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("NOT YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertIn("NOT YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_baba_is_you(self):
        r1 = self.game.get_rule("NOT BABA IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_baba_is_not_you(self):
        r1 = self.game.get_rule("NOT BABA IS NOT YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("NOT YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("NOT YOU", keke["IS"], "KEKE IS NOT NOT YOU")
        self.assertNotIn("NOT YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_red_baba_is_you(self):
        r1 = self.game.get_rule("RED BABA IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_not_red_baba_is_you(self):
        r1 = self.game.get_rule("NOT RED BABA IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_baba_and_keke_is_you(self):
        r1 = self.game.get_rule("BABA AND KEKE IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_keke_and_baba_is_you(self):
        r1 = self.game.get_rule("KEKE AND BABA IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_and_not_keke_is_you(self):
        r1 = self.game.get_rule("BABA AND NOT KEKE IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_not_red_baba_and_keke_is_you(self):
        r1 = self.game.get_rule("NOT RED BABA AND KEKE IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

    def test_not_baba_and_not_keke_is_you(self):
        r1 = self.game.get_rule("NOT BABA AND NOT KEKE IS YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

    def test_baba_is_you_and_red(self):
        r1 = self.game.get_rule("BABA IS YOU AND RED")
        self.game.apply_rule(r1)

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
        r1 = self.game.get_rule("BABA IS YOU AND NOT RED")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

        self.assertIn("NOT RED", baba["IS"], "BABA IS NOT NOT RED")
        self.assertNotIn("NOT RED", keke["IS"], "KEKE IS NOT RED")
        self.assertIn("NOT RED", red_baba["IS"], "RED BABA IS NOT NOT RED")

    def test_baba_is_you_and_not_you(self):
        r1 = self.game.get_rule("BABA IS YOU AND NOT YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        keke = self.game.entities[1]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", keke["IS"], "KEKE IS YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

        self.assertIn("NOT YOU", baba["IS"], "BABA IS RED")
        self.assertIn("NOT YOU", keke["IS"], "KEKE IS NOT YOU")
        self.assertIn("NOT YOU", red_baba["IS"], "RED BABA IS RED")

    def test_baba_is_not_not_you(self):
        r1 = self.game.get_rule("BABA IS NOT NOT YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        red_baba = self.game.entities[2]

        self.assertIn("YOU", baba["IS"], "BABA IS NOT YOU")
        self.assertIn("YOU", red_baba["IS"], "RED BABA IS NOT YOU")

        self.assertNotIn("NOT YOU", baba["IS"], "BABA IS NOT RED")
        self.assertNotIn("NOT YOU", red_baba["IS"], "RED BABA IS NOT RED")

        self.assertNotIn("NOT NOT YOU", baba["IS"], "BABA IS NOT NOT RED")
        self.assertNotIn("NOT NOT YOU", red_baba["IS"], "RED BABA IS NOT NOT RED")

    def test_baba_is_not_not_not_you(self):
        r1 = self.game.get_rule("BABA IS NOT NOT NOT YOU")
        self.game.apply_rule(r1)

        baba = self.game.entities[0]
        red_baba = self.game.entities[2]

        self.assertNotIn("YOU", baba["IS"], "BABA IS YOU")
        self.assertNotIn("YOU", red_baba["IS"], "RED BABA IS YOU")

        self.assertIn("NOT YOU", baba["IS"], "BABA IS NOT NOT RED")
        self.assertIn("NOT YOU", red_baba["IS"], "RED BABA IS NOT NOT RED")

        self.assertNotIn("NOT NOT YOU", baba["IS"], "BABA IS NOT NOT RED")
        self.assertNotIn("NOT NOT YOU", red_baba["IS"], "RED BABA IS NOT NOT RED")

        self.assertNotIn("NOT NOT NOT YOU", baba["IS"], "BABA IS NOT NOT NOT RED")
        self.assertNotIn("NOT NOT NOT YOU", red_baba["IS"], "RED BABA IS NOT NOT NOT RED")


if __name__ == "__main__":
    unittest.main()

