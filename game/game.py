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
                "PART": set(["NOUN"]),
            },
            "KEKE": {
                "PART": set(["NOUN"]),
            },
            "ALL": {
                "PART": set(["NOUN"]),
                "ACTION": {"NOUN": "ALL"},
            },
            "NONE": {
                "PART": set(["NOUN"]),
                "ACTION": {"NOUN": "NONE"},
            },
            "IS": {
                "PART": set(["VERB"]),
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 100,
                        "LEFT": set(["NOUN"]),
                        "RIGHT": set(["PROPERTY"]),
                        "PART": set(["SENTENCE"]),
                        "ACTION": {"SENTENCE": "GIVE"}
                    },
                    {
                        "PRIORITY": 100.1,
                        "LEFT": set(["NOUN"]),
                        "RIGHT": set(["ADJECTIVE"]),
                        "PART": set(["SENTENCE"]),
                        "ACTION": {"SENTENCE": "GIVE"}
                    }
                ]
            },
            "NOT": {
                "PART": set(["ADVERB"]),
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 0.1,
                        "RIGHT": set(["NOUN", "PROPERTY", "ADJECTIVE"]),
                        "ACTION": "NEGATE",
                        "PART": "RIGHT"
                    },
                ]
            },
            "AND": {
                "PART": set(["CONJUNCTION"]),
                "SIMPLIFICATION": [
                    {
                        "PRIORITY": 10,
                        "LEFT": set(["ADJECTIVE"]),
                        "RIGHT": set(["ADJECTIVE"]),
                        "PART": set(["ADJECTIVE"]),
                        "ACTION": {"ADJECTIVE": "AND"}
                    },
                    {
                        "PRIORITY": 10.1,
                        "LEFT": set(["PROPERTY"]),
                        "RIGHT": set(["PROPERTY"]),
                        "PART": set(["PROPERTY"]),
                        "ACTION": {"PROPERTY": "AND"}
                    }
                ]
            },
            "YOU": {
                "PART": set(["PROPERTY"])
            },
            "RED": {
                "PART": set(["ADJECTIVE", "PROPERTY"])
            }
        }

        self.parts = {
            "NOUN": {
                "ACTION": "SELECT",
            },
            "VERB": {},
            "PROPERTY": {
                "ACTION": "GET",
            },
            "ADJECTIVE": {
                "ACTION": "SPECIFY",
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
        self.primitive_act(self.get_action(rule), rule, ents=self.entities)

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
                "SIMPLIFICATION": self.words[t].get("SIMPLIFICATION", [])
            }
            for t in txt.split(" ")
        ]

        for token in tokens:
            token["ACTION"] = {}
            for part in token["PART"]:
                token["ACTION"][part] = self.parts[part].get("ACTION", None)
            if "ACTION" in self.words[token["TEXT"]].keys():
                acts = self.words[token["TEXT"]]["ACTION"]
                for part, action in acts.items():
                    token["ACTION"][part] = action

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
        for part in token["PART"]:
            all_simplifications.extend(
                self.parts[part].get("SIMPLIFICATION", [])
            )

        pos_simplifications = []
        for simp in all_simplifications:
            left = simp.get("LEFT", None)
            right = simp.get("RIGHT", None)

            left_inter = None
            right_inter = None

            if left is not None and token["LEFT"] is not None:
                left_inter = left.intersection(token["LEFT"]["PART"])
            if right is not None and token["RIGHT"] is not None:
                right_inter = right.intersection(token["RIGHT"]["PART"])

            if left_inter is not None and len(left_inter) == 0:
                continue
            if right_inter is not None and len(right_inter) == 0:
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

        if type(new_action) is str:
            a = {}
            for part in new_part:
                a[part] = new_action
            new_action = a

        new_left = token["LEFT"]
        new_right = token["RIGHT"]

        if "LEFT" in simp.keys():
            new_token["TEXT"] += token["LEFT"]["TEXT"] + " "
            new_left = token["LEFT"]["LEFT"]
            token["LEFT"]["PART"] = simp["LEFT"].intersection(token["LEFT"]["PART"])
            # Simple trick to help determine root elements.
            token["LEFT"]["LEFT"] = None

        new_token["TEXT"] += token["TEXT"]

        if "RIGHT" in simp.keys():
            new_token["TEXT"] += " " + token["RIGHT"]["TEXT"]
            new_right = token["RIGHT"]["RIGHT"]
            token["RIGHT"]["PART"] = simp["RIGHT"].intersection(token["RIGHT"]["PART"])
            # Simple trick to help determine root elements.
            token["RIGHT"]["RIGHT"] = None

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

    def get_action(self, token, part=None):
        if part is None:
            part = list(token["PART"])[0]
        return token["ACTION"][part]

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

    """
    def get_root_tokens(self, tokens, prev=None):
        roots = []
        for token in tokens:
            if token["ROOT"] is None:
                roots.append(token)

                walk_through = [token["LEFT"], token["RIGHT"]]
                walk_through = [t for t in walk_through if t != prev and t is not None]

                for t in self.get_root_tokens(walk_through, prev=token):
                    roots.append(t)

                continue

            for t in self.get_root_tokens([token["ROOT"]], prev=token):
                roots.append(t)
        return roots
    """
