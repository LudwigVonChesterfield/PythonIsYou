# Entity

{
	"TEXT": string,
	"IS": set(string),
	"HAS": list(object(Entity))
}

# Simplification

{
	"PRIORITY": float,
	"LEFT": string(PART),
	"RIGHT": stirng(PART),
	"PART": string(PART), // LEFT - keep LEFT's part, RIGHT - keep RIGHT's part.
	"ACTION": string(ACTION), // string(ACTION) to set all possible part-actions to that action
}

# Part

{
	"SIMPLIFICATION": list(object(Simplification))
}

# Word

{
	"PART": string(PART),
	"ACTION": string(ACTION)),
	"SIMPLIFICATION": list(object(Simplification))
}

# Token

{
	"TEXT": string,
	"PART": string(PART),
	"ACTION": string(ACTION),
	"LEFT": object(Token),
	"RIGHT": object(Token),
	"ROOT": object(Token),
	"SIMPLIFICATION": list(object(Simplification))
}

# Part

# Action (TO-DO)

{
	"TYPE": "ACTION"

	???
}

# Primitive Actions

{
	"TYPE": "PRIMITIVE",
}
