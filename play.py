import game.game as g

game = g.Game(
    debug=True,
    debug_options={
        "PRINT_TREEIFY_KEYS": ["TEXT"]
    }
)
game.entities.append(
    {
        "TEXT": "BABA",
        "IS": set(["RED"]),
        "HAS": []
    }
)

r1 = game.get_rule("NOT BABA IS YOU")

print(
    game.cols_from(
        [r1],
        ["TEXT"]
    )
)

game.add_rule(r1)

"""
while True:
    game.update_rules()
"""
