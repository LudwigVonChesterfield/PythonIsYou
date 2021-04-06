class Primitive_Actions:
    @classmethod
    def ALL(cls, game, entities, token):
        return list(entities)

    @classmethod
    def NONE(cls, game, entities, token):
        return []

    @classmethod
    def SELECT(cls, game, entities, token):
        return [
            entity for entity
            in entities
            if entity["TEXT"] == token["TEXT"]
        ]

    @classmethod
    def SPECIFY(cls, game, entities, token):
        if token["ROOT"]["ACTION"] == "SELECT":
            return [
                entity for entity
                in cls.SELECT(game, entities, token["ROOT"])
                if token["LEFT"]["TEXT"] in entity["IS"]
            ]

        return [
            entity for entity
            in cls.SPECIFY(game, entities, token["ROOT"])
            if token["LEFT"]["TEXT"] in entity["IS"]
        ]

    @classmethod
    def GET(cls, game, entities, token):
        return [token["TEXT"]]

    @classmethod
    def GIVE(cls, game, entities, token):
        selected = game.primitive_act(
            game.get_action(token["ROOT"]["LEFT"]),
            token["ROOT"]["LEFT"],
            ents=entities
        )
        properties = game.primitive_act(
            game.get_action(token["ROOT"]["RIGHT"]),
            token["ROOT"]["RIGHT"],
            ents=entities
        )

        for ent in selected:
            for prop in properties:
                ent["IS"].add(prop)

    @classmethod
    def AND(cls, game, entities, token):
        first = game.primitive_act(
            game.get_action(token["ROOT"]["LEFT"]),
            token["ROOT"]["LEFT"],
            ents=entities
        )
        second = game.primitive_act(
            game.get_action(token["ROOT"]["RIGHT"]),
            token["ROOT"]["RIGHT"],
            ents=entities
        )

        first.extend(second)
        return first

    @classmethod
    def NEGATE(cls, game, entities, token):
        if game.get_action(token["ROOT"]["RIGHT"], list(token["PART"])[0]) == "GET":
            return [
                "NOT " + t
                for t in game.primitive_act(
                    game.get_action(token["ROOT"]["RIGHT"]),
                    token["ROOT"]["RIGHT"],
                    ents=entities
                )
            ]
        if game.get_action(token["ROOT"]["RIGHT"], list(token["PART"])[0]) == "NEGATE":
            return game.primitive_act(
                game.get_action(token["ROOT"]["RIGHT"]["ROOT"]["RIGHT"]),
                token["ROOT"]["RIGHT"]["ROOT"]["RIGHT"],
                ents=entities
            )

        return [
            t
            for t in game.primitive_act(
                game.get_action(token["ROOT"]["RIGHT"]),
                token["ROOT"]["RIGHT"],
                ents=entities
            )
            if t not in entities
        ]
