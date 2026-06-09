from smolagents import OpenAIModel,ToolCallingAgent, CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, load_tool, tool
from dotenv import load_dotenv
load_dotenv()

@tool
def extract_population(search_result: str) -> int:
    """
    Extracts the population number from a text.

    Args:
        search_result (str): The text returned by the search tool containing population information.

    Returns:
        int: The population number of the country.
    """
    import re
    numbers = re.findall(r'\d[\d,]*', search_result)
    if numbers:
        return int(numbers[0].replace(',', ''))
    return 0


@tool
def calculate_growth(previous_pop: int, current_pop: int) -> float:
    """
    Calculates the percentage increase between previous and current population.

    Args:
        previous_pop (int): Population in the previous year.
        current_pop (int): Population in the current year.

    Returns:
        float: Percentage growth between the two populations.
    """
    if previous_pop == 0:
        return 0.0
    return ((current_pop - previous_pop) / previous_pop) * 100


@tool
def compare_population_growth(country1: str, pop1: int, growth1: float,
                              country2: str, pop2: int, growth2: float) -> str:
    """
    Compares two countries by population and growth rate.

    Args:
        country1 (str): Name of the first country.
        pop1 (int): Population of the first country.
        growth1 (float): Growth rate of the first country.
        country2 (str): Name of the second country.
        pop2 (int): Population of the second country.
        growth2 (float): Growth rate of the second country.

    Returns:
        str: Comparison summary between the two countries.
    """
    pop_result = f"{country1} ({pop1}) vs {country2} ({pop2})"
    growth_result = f"{country1} growth: {growth1:.2f}% vs {country2} growth: {growth2:.2f}%"

    if pop1 > pop2:
        pop_winner = f"{country1} greater in population"
    elif pop2 > pop1:
        pop_winner = f"{country2} greater in population"
    else:
        pop_winner = "The population is equal"

    if growth1 > growth2:
        growth_winner = f"{country1} With a higher growth rate"
    elif growth2 > growth1:
        growth_winner = f"{country2} With a higher growth rate"
    else:
        growth_winner = "The growth rate is equal"

    return f"{pop_result}\n{growth_result}\n{pop_winner}, {growth_winner}"



final_answer=FinalAnswerTool()
search_tool = DuckDuckGoSearchTool()

model=OpenAIModel(
    model_id="gpt-4.1-mini"
)

agent=ToolCallingAgent(
    model=model,
    tools=[final_answer,search_tool,extract_population,calculate_growth],
    max_steps=5,
)

agent_code=CodeAgent(
    model=model,
    tools=[final_answer,search_tool,extract_population],
    max_steps=5
)

# result = agent_code.run("Compare Israel and USA by population and growth rate.")
# print(result)

result = agent.run("Compare Israel and USA by population and growth rate.")
print(result)
