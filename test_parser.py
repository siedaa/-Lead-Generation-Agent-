from dotenv import load_dotenv

load_dotenv()

from agent.parser import parse_prompt

samples = [
    "coffee shops in America",
    "find me dentists near Boston",
    "restaurants in New York City",
    "plumbers Chicago",
    "gyms in downtown Karachi",
]

for s in samples:
    result = parse_prompt(s)
    print(f"Input:  {s}")
    print(f"Output: {result}")
    print()