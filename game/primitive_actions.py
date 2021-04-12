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
                if token["ROOT"]["LEFT"]["TEXT"] in entity["IS"]
            ]

        return [
            entity for entity
            in cls.SPECIFY(game, entities, token["ROOT"])
            if token["ROOT"]["LEFT"]["TEXT"] in entity["IS"]
        ]

    @classmethod
    def GET(cls, game, entities, token):
        return [token["TEXT"]]

    @classmethod
    def GIVE(cls, game, entities, token):
        selected = game.primitive_act(
            token["ROOT"]["LEFT"]["ACTION"],
            token["ROOT"]["LEFT"],
            ents=entities
        )
        properties = game.primitive_act(
            token["ROOT"]["RIGHT"]["ACTION"],
            token["ROOT"]["RIGHT"],
            ents=entities
        )

        for ent in selected:
            for prop in properties:
                ent["IS"].add(prop)

    @classmethod
    def AND(cls, game, entities, token):
        first = game.primitive_act(
            token["ROOT"]["LEFT"]["ACTION"],
            token["ROOT"]["LEFT"],
            ents=entities
        )
        second = game.primitive_act(
            token["ROOT"]["RIGHT"]["ACTION"],
            token["ROOT"]["RIGHT"],
            ents=entities
        )

        first.extend(second)

        return first

    @classmethod
    def NEGATE(cls, game, entities, token):
        if token["ROOT"]["RIGHT"]["ACTION"] == "GET":
            return [
                "NOT " + t
                for t in game.primitive_act(
                    token["ROOT"]["RIGHT"]["ACTION"],
                    token["ROOT"]["RIGHT"],
                    ents=entities
                )
            ]
        if token["ROOT"]["RIGHT"]["ACTION"] == "NEGATE":
            return game.primitive_act(
                token["ROOT"]["RIGHT"]["ROOT"]["RIGHT"]["ACTION"],
                token["ROOT"]["RIGHT"]["ROOT"]["RIGHT"],
                ents=entities
            )

        not_entities = game.primitive_act(
            token["ROOT"]["RIGHT"]["ACTION"],
            token["ROOT"]["RIGHT"],
            ents=entities
        )
        return [
            t
            for t in entities
            if t not in not_entities
        ]
