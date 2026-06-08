"""Financial concepts — JARVIS explains financial terms and concepts clearly."""
import random

_CONCEPTS = {
    "inflation": "Inflation is the rate at which prices rise over time, eroding purchasing power. Central banks target ~2% annually, sir.",
    "recession": "A recession is two consecutive quarters of negative GDP growth. Typically involves rising unemployment and falling spending, sir.",
    "bull market": "A bull market is a sustained period of rising asset prices, typically 20%+ gains. Driven by optimism and strong fundamentals, sir.",
    "bear market": "A bear market is a 20%+ decline from recent highs. Driven by pessimism, economic weakness, or external shocks, sir.",
    "etf": "An ETF (Exchange-Traded Fund) is a basket of securities traded on an exchange. Low cost, diversified, and liquid, sir.",
    "compound interest": "Compound interest earns interest on your interest. Einstein called it the eighth wonder of the world, sir.",
    "dividend": "A dividend is a portion of company profits paid to shareholders. Typically quarterly. A sign of financial health, sir.",
    "p/e ratio": "The Price-to-Earnings ratio compares share price to earnings. A high P/E suggests growth expectations; low suggests value, sir.",
    "hedge fund": "A hedge fund is a private investment partnership using diverse strategies to generate returns regardless of market direction, sir.",
    "ipo": "An IPO (Initial Public Offering) is when a private company first sells shares to the public on a stock exchange, sir.",
    "liquidity": "Liquidity refers to how quickly an asset can be converted to cash without significant price impact, sir.",
    "volatility": "Volatility measures how much an asset's price fluctuates. Higher volatility = higher risk and potential reward, sir.",
}

_TIPS = [
    "Time in the market beats timing the market — stay invested, sir.",
    "Diversification reduces risk without necessarily reducing returns, sir.",
    "Keep 3-6 months expenses as an emergency fund before investing, sir.",
    "Fees compound just like returns — minimise them wherever possible, sir.",
    "Invest consistently regardless of market conditions — dollar cost averaging, sir.",
    "Understand what you invest in. If you can't explain it, don't buy it, sir.",
]

def explain(concept: str) -> str:
    for key, desc in _CONCEPTS.items():
        if key in concept.lower() or concept.lower() in key:
            return desc
    return f"Concept '{concept}' not in database. Available: {', '.join(_CONCEPTS.keys())}, sir."

def get_tip() -> str:
    return random.choice(_TIPS)

def list_concepts() -> str:
    return f"Financial concepts: {', '.join(_CONCEPTS.keys())}, sir."
