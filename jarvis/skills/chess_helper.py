"""Chess helper — JARVIS explains chess moves and openings."""
_OPENINGS = {
    "sicilian": "The Sicilian Defence (1.e4 c5) is the most popular response to e4, leading to sharp, asymmetrical play, sir.",
    "london":   "The London System (1.d4 2.Nf3 3.Bf4) is a solid, quiet opening — reliable for beginners and grandmasters alike, sir.",
    "french":   "The French Defence (1.e4 e6) creates a solid pawn structure but can be passive early on, sir.",
    "ruy lopez":"The Ruy López (1.e4 e5 2.Nf3 3.Bb5) has been played for centuries — a classic attacking opening, sir.",
    "kings gambit": "The King's Gambit (1.e4 e5 2.f4) is aggressive and romantic — sacrifice a pawn for rapid development, sir.",
    "queens gambit": "The Queen's Gambit (1.d4 d5 2.c4) offers a pawn to gain central control — not a true gambit, sir.",
    "caro kann": "The Caro-Kann (1.e4 c6) is solid and reliable — Black gives up some space for structural integrity, sir.",
}

_TIPS = [
    "Control the centre in the opening with pawns and pieces, sir.",
    "Castle early to protect your king, sir.",
    "Connect your rooks by clearing the back rank, sir.",
    "Knights are strongest in the centre, not on the edge, sir.",
    "In the endgame, activate your king — it becomes a powerful piece, sir.",
    "Trade pieces when you're ahead; keep pieces when you're behind, sir.",
    "Always ask: what is my opponent threatening? Before you move, sir.",
]

def get_opening(name: str) -> str:
    for key, desc in _OPENINGS.items():
        if key in name.lower():
            return desc
    openings = ", ".join(_OPENINGS.keys())
    return f"Opening not found. Known openings: {openings}, sir."

def get_tip() -> str:
    import random
    return random.choice(_TIPS)

def explain_piece(piece: str) -> str:
    pieces = {
        "pawn": "Pawns move forward one square, capture diagonally. They're the soul of chess — control the centre with them, sir.",
        "knight": "Knights move in an L-shape and are the only piece that can jump over others. Worth ~3 pawns, sir.",
        "bishop": "Bishops move diagonally any number of squares. Each controls only one colour — worth ~3 pawns, sir.",
        "rook": "Rooks move horizontally and vertically any number of squares. Worth ~5 pawns — dominant in open files, sir.",
        "queen": "The queen moves in any direction any number of squares. The most powerful piece — worth ~9 pawns, sir.",
        "king": "The king moves one square in any direction. Protect it in the middlegame, activate it in the endgame, sir.",
    }
    for key, desc in pieces.items():
        if key in piece.lower():
            return desc
    return f"Piece '{piece}' not recognised, sir."
