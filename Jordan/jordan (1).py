# jordan.py

"""
Jordanian Railway Chronicles Simulator

In this assignment, you will simulate the construction of a railway network in 
Jordan during the year 1916. 

Your task:
-----------
Determine the cheapest order to construct nine railway stations so that the 
total construction cost does not exceed a given budget.

Rules:
------
1. Each station has a base construction cost (see STATION_COSTS dictionary).
2. The final cost of building a station depends on:
   - The previously constructed station.
   - The last digit of your student ID.

Formula for station cost:
    Final Cost = Base Cost_current +
                 Base Cost_previous * (SID + 1)^1.3 *
                 (1 + 0.07 * (Index of Current Station % 3))

Steps to complete:
------------------
- Implement each function as described in its docstring.
- Use loops or permutations to explore possible station orders.
- Return the cheapest valid order that fits within the budget.

Note:
-----
Partial marks will be awarded if your solution finds *a valid* order within 
budget, even if it is not the absolute cheapest.
"""

# -------------------- Part 1: Global Variable -------------------- #

STATION_COSTS = {
    # TODO: Fill in the nine stations with their base costs.
    # Example:
    # 'Amman': 12,
    # 'Petra': 8,
    # ...
    "Amman": 12,
    "Petra": 8,
    "Karak": 10,
    "Irbid": 7,
    "Salt": 6,
    "Aqaba": 9,
    "Jerash": 11,
    "Madaba": 7,
    "Mafraq": 8
}

import itertools

# -------------------- Part 2: Functions -------------------- #

def is_valid_sid(sid: str) -> bool:
    """
    Checks whether the provided student ID (SID) is valid.

    A valid SID must:
    - Be numeric.
    - Contain exactly 9 characters.

    Parameters:
        sid (str): The student ID to validate.

    Returns:
        bool: True if the SID is valid, False otherwise.
    """
    return sid.isnumeric() and len(sid) == 9


def calculate_station_cost(current_station: str, previous_station: str, sid_last_digit: int) -> float:
    """
    Calculates the final cost of constructing a station based on a dynamic pricing 
    mechanism.

    Formula:
        Final Cost = Base Cost_current + 
                     Base Cost_previous * (SID + 1)^1.3 * 
                     (1 + 0.07 * (Index of Current Station % 3))

    Parameters:
        current_station (str): The name of the current station.
        previous_station (str): The name of the previously constructed station.
        sid_last_digit (int): The last digit of the student ID (0-9).

    Returns:
        float: The final calculated cost of constructing the current station.
    """
    # Get base costs
    base_current = STATION_COSTS[current_station]
    base_previous = STATION_COSTS[previous_station]

    # Get index of current station in dictionary order
    station_names = list(STATION_COSTS.keys())
    index_current = station_names.index(current_station)

    # Apply formula
    final_cost = base_current + base_previous * ((sid_last_digit + 1) ** 1.3) * (1 + 0.07 * (index_current % 3))

    return final_cost


def calculate_total_order_cost(order: list[str], sid_last_digit: int) -> float:
    """
    Calculates the total cost of constructing a complete sequence of stations.

    The cost of each station is calculated based on its position in the order:
    - The first station uses its base cost.
    - All others use calculate_station_cost() with the previously built station.

    Parameters:
        order (list[str]): The list of stations in construction order.
        sid_last_digit (int): The last digit of the student ID (0-9).

    Returns:
        float: The total cost of constructing the entire railway.
    """
    if not order:  
        return 0.0

    # first station
    total_cost = STATION_COSTS[order[0]]

    # second station
    for i in range(1, len(order)):
        current = order[i]
        previous = order[i - 1]
        total_cost += calculate_station_cost(current, previous, sid_last_digit)

    return total_cost


def build_railway(stations: list[str], sid_last_digit: int, budget: int) -> list[str]:
    """
    Explores every possible order of constructing stations and returns the 
    sequence with the lowest total cost that does not exceed the budget.

    Partial marks can be awarded if it returns a valid order that isn't the
    absolute cheapest but still fits within the budget.

    Parameters:
        stations (list[str]): A list of stations left to construct.
        sid_last_digit (int): The last digit of the student ID.
        budget (int): Maximum allowable total construction cost.

    Returns:
        list[str]: The order of stations to construct, or empty list if none
        is possible.
    """
    cheapest_order = []
    cheapest_cost = float('inf')

    # Try every possible permutation (9! = 362,880)
    for order in itertools.permutations(stations):
        total_cost = calculate_total_order_cost(order, sid_last_digit)

        if total_cost <= budget and total_cost < cheapest_cost:
            cheapest_cost = total_cost
            cheapest_order = list(order)

    return cheapest_order

def find_affordable_railway(stations: list[str], sid_last_digit: int, budgets: list[int]) -> list[str]:
    """
    Attempts to find a valid railway construction order by testing multiple budgets.

    The function should:
      - Iterate through `budgets` in the given order.
      - Use `continue` to skip budgets that are obviously too low.
      - Use `break` to stop searching after the first budget that allows a full
        valid railway order.
      - Return the valid order found for that first sufficient budget.
      - If no budget allows a full railway, return an empty list.

    Parameters:
        stations (list[str]): List of station names to consider.
        sid_last_digit (int): The last digit of the student ID (0-9).
        budgets (list[int]): A list of budgets to try (e.g. [100, 150, 200]).

    Returns:
        list[str]: The first valid railway order found within the budgets,
                   or an empty list if none are sufficient.

    Notes for students:
        - Do not hardcode budget thresholds; you may compute a heuristic minimum
          (e.g., sum of base costs) and use it to decide whether to `continue`.
        - Make sure you apply advanced control flows your loop logic (these constructs are being assessed).
    """
    base_minimum = sum(STATION_COSTS.values())
    for budget in budgets:
        if budget < base_minimum:
            print(f"Budget {budget} too low, skipping...")
            continue

        order = build_railway(stations, sid_last_digit, budget)

        if order:
            print(f"Valid railway order found for budget {budget}:")
            return order  
    return []


# -------------------- Part 3: Sample Execution -------------------- #

if __name__ == "__main__":
    # Example placeholders for testing:
    sid = "123456789"
    sid_last_digit = int(sid[-1])  
    budgets = [100, 200, 500]
    stations = list(STATION_COSTS.keys())

    if not is_valid_sid(sid):
        print("Invalid student ID!")
    else:
        order = find_affordable_railway(stations, sid_last_digit, budgets)
        if order:
            total_cost = calculate_total_order_cost(order, sid_last_digit)
            print("Cheapest order:", order)
            print("Total cost:", round(total_cost, 2))
        else:
            print("No valid order found for any budget.")

    # TODO: Uncomment and test after implementing the functions
    # if not is_valid_sid(sid):
    #     print("Invalid student ID!")
    # else:
    #     order = find_affordable_railway(stations, sid_last_digit, budgets)
    #     if order:
    #         total_cost = calculate_total_order_cost(order, sid_last_digit)
    #         print("Cheapest order:", order)
    #         print("Total cost:", round(total_cost, 2))
    #     else:
    #         print("No valid order found for any budget.")

