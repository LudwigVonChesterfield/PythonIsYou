import game.game as g

game = g.Game(debug=True)

r1 = game.get_rule("BABA IS YOU AND RED")

print(
    game.cols_from(
        [r1],
        ["TEXT", "PART", "ACTION"]
    )
)

game.apply_rule(r1)
print(game.entities)
