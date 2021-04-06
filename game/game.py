import traceback

from heapq import heapify, heappop

from .primitive_actions import Primitive_Actions


"""
TO-DO: support multiple part-of-speech per word?
thus: make action associative word["ACTION"][part] -> action
"""


class Game:
    def __init__(self, debug=False):
        self.debug = debug

        self.words = {
            "BABA": {
                "PART": "NOUN",
            },
            "KEKE": {
                "PART": "NOUN",
            },
            "ALL": {
                "PART": "NOUN",
                "ACTION": "ALL",
            },
            "NONE": {
                "PART": "NOUN",
                "ACTION": "NONE",
            },
            "IS": {
                "PART": "VERB",

                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 100,
                        "LEFT": "NOUN",
                        "RIGHT": "PROPERTY",
                        "PART": "SENTENCE",
                        "ACTION": "GIVE"
                    },
                    {
                        "PRIORITY": 100.1,
                        "LEFT": "NOUN",
                        "RIGHT": "ADJECTIVE",
                        "PART": "SENTENCE",
                        "ACTION": "GIVE"
                    }
                ]
            },
            "NOT": {
                "PART": "ADVERB",
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 0,
                        "RIGHT": "NOUN",
                        "ACTION": "NEGATE",
                        "PART": "RIGHT"
                    },
                    {
                        "PRIORITY": 0.1,
                        "RIGHT": "PROPERTY",
                        "ACTION": "NEGATE",
                        "PART": "PROPERTY"
                    },
                    {
                        "PRIORITY": 0.2,
                        "RIGHT": "ADJECTIVE",
                        "ACTION": "NEGATE",
                        "PART": "ADJECTIVE"
                    },
                ]
            },
            "AND": {
                "PART": "CONJUNCTION",
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 10,
                        "LEFT": "ADJECTIVE",
                        "RIGHT": "ADJECTIVE",
                        "PART": "ADJECTIVE",
                        "ACTION": "AND"
                    },
                    {
                        "PRIORITY": 10.1,
                        "LEFT": "PROPERTY",
                        "RIGHT": "PROPERTY",
                        "PART": "PROPERTY",
                        "ACTION": "AND"
                    },
                    {
                        "PRIORITY": 10.2,
                        "LEFT": "PROPERTY",
                        "RIGHT": "PROPERTY",
                        "PART": "PROPERTY",
                        "ACTION": "AND"
                    },
                    {
                        "PRIORITY": 10.3,
                        "LEFT": "PROPERTY",
                        "RIGHT": "PROPERTY",
                        "PART": "PROPERTY",
                        "ACTION": "AND"
                    }
                ]
            },
            "YOU": {
                "PART": "PROPERTY",
            },
            "RED": {
                "PART": "ADJECTIVE",
            }
        }

        self.parts = {
            "NOUN": {
                "ACTION": "SELECT",
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 1,
                        "LEFT": "ADJECTIVE",
                        "ACTION": "SPECIFY"
                    }
                ]
            },
            "VERB": {},
            "PROPERTY": {
                "ACTION": "GET",
            },
            "ADJECTIVE": {
                "ACTION": "GET",
            },
            "ADVERB": {},
            "CONJUNCTION": {},
            "SENTENCE": {}
        }

        self.actions = {

        }

        self.primitives = {
            "ALL": Primitive_Actions.ALL,
            "NONE": Primitive_Actions.NONE,
            "SELECT": Primitive_Actions.SELECT,
            "SPECIFY": Primitive_Actions.SPECIFY,
            "GET": Primitive_Actions.GET,
            "GIVE": Primitive_Actions.GIVE,
            "AND": Primitive_Actions.AND,
            "NEGATE": Primitive_Actions.NEGATE
        }

        self.entities = [
            {
                "TEXT": "BABA",
                "IS": set([]),
                "HAS": []
            },
            {
                "TEXT": "KEKE",
                "IS": set([]),
                "HAS": []
            }
        ]

    def get_rule(self, txt):
        try:
            tokens = self.tokenify(txt)
            tree = self.treeify(tokens)

            if len(tree) == 0:
                return {}

            if "SENTENCE" not in tree[0]["PART"]:
                return {}

        except Exception:
            if self.debug:
                traceback.print_exc()

            return {}

        return tree[0]

    def apply_rule(self, rule):
        # TO-DO: support complex actions.
        self.primitive_act(rule["ACTION"], rule, ents=self.entities)

    def update_rules():
        for rule in self.rules:
            self.apply_rule(rule)

    def add_rule(self, rule):
        self.rules.append(rule)
        self.update_rules()

    def primitive_act(self, action, token, ents=None):
        if ents is None:
            ents = self.entities
        return self.primitives[action](self, ents, token)

    def tokenify(self, txt):
        tokens = [
            {
                "TEXT": t,
                "PART": self.words[t]["PART"],
                "LEFT": None,
                "RIGHT": None,
                "ROOT": None,
                "ACTION": self.words[t].get(
                    "ACTION", self.parts[self.words[t]["PART"]].get("ACTION", None)
                ),
                "SIMPLIFICATION": self.words[t].get("SIMPLIFICATION", [])
            }
            for t in txt.split(" ")
        ]

        prev = None
        for i in range(len(tokens)):
            token = tokens[i]

            token["LEFT"] = prev
            if prev is not None:
                prev["RIGHT"] = token

            prev = token

        return tokens

    def get_simplification(self, token):
        all_simplifications = []
        all_simplifications.extend(
            token.get("SIMPLIFICATION", [])
        )
        all_simplifications.extend(
            self.parts[token["PART"]].get("SIMPLIFICATION", [])
        )

        pos_simplifications = []
        for simp in all_simplifications:
            left = simp.get("LEFT", None)
            right = simp.get("RIGHT", None)

            if left is not None and (token["LEFT"] is None or token["LEFT"]["PART"] != left):
                continue
            if right is not None and (token["RIGHT"] is None or token["RIGHT"]["PART"] != right):
                continue

            pos_simplifications.append((simp["PRIORITY"], simp))

        if len(pos_simplifications) == 0:
            return {}

        heapify(pos_simplifications)

        return heappop(pos_simplifications)[1]

    def simplify_token(self, token, simp):
        new_token = {"TEXT": "", "ROOT": token}

        new_part = simp.get("PART", token["PART"])
        new_action = simp.get("ACTION", token["ACTION"])

        if new_part == "LEFT":
            new_part = token["LEFT"]["PART"]

        if new_part == "RIGHT":
            new_part = token["RIGHT"]["PART"]

        new_left = token["LEFT"]
        new_right = token["RIGHT"]

        if "LEFT" in simp.keys():
            new_token["TEXT"] += token["LEFT"]["TEXT"] + " "
            new_left = token["LEFT"]["LEFT"]

        new_token["TEXT"] += token["TEXT"]

        if "RIGHT" in simp.keys():
            new_token["TEXT"] += " " + token["RIGHT"]["TEXT"]
            new_right = token["RIGHT"]["RIGHT"]

        new_token["PART"] = new_part
        new_token["ACTION"] = new_action

        new_token["LEFT"] = new_left
        new_token["RIGHT"] = new_right

        new_token["SIMPLIFICATION"] = []

        if new_left is not None:
            new_left["RIGHT"] = new_token
        if new_right is not None:
            new_right["LEFT"] = new_token

        return new_token

    def simplify(self, tokens):
        pos_simplifications = []

        for i, token in enumerate(tokens):
            simp = self.get_simplification(token)
            if "PRIORITY" not in simp.keys():
                continue
            pos_simplifications.append((simp["PRIORITY"], i, simp))

        if len(pos_simplifications) == 0:
            return tokens, True

        heapify(pos_simplifications)
        prio, ind, simp = heappop(pos_simplifications)
        token = tokens[ind]

        new_token = self.simplify_token(token, simp)

        new_tokens = []

        first = new_token
        while first["LEFT"] is not None:
            first = first["LEFT"]

        last = first
        while last is not None:
            new_tokens.append(last)
            last = last["RIGHT"]

        return new_tokens, False

    def treeify(self, tokens, tries=5):
        done = False
        i = 0

        while not done and i < tries:
            if self.debug:
                print(
                    self.cols_from(
                        tokens,
                        ["TEXT", "PART", "ACTION"]
                    )
                )
            tokens, done = self.simplify(tokens)

            i += 1

        return tokens

    def cols_from(self, tokens, cols):
        def get_from_col(t, col):
            if type(col) is str:
                return t[col]
            else:
                r = t
                for c in col:
                    if r is None:
                        break
                    r = r[c]
                return r

        return [
            dict([
                (k, get_from_col(t, k))
                for k in cols
            ])
            for t in tokens
        ]
