'''
australia.py

A program that simulates the relocation of Australian animals across states.

Each animal has a known threat to avoid. The goal is to relocate as many 
animals as possible while ensuring that no animal ends up near its threat — 
and no two animals share the same state.

This program involves reading animal data from a file, building objects to
represent each animal, and implementing relocation logic to ensure animals
are placed safely.
'''


ADJACENT_STATES = {
    "NSW": ["VIC", "SA", "QLD"],
    "QLD": ["NT", "SA", "NSW"],
    "VIC": ["SA", "NSW"],
    "TAS": [],
    "SA": ["WA", "NT", "QLD", "NSW", "VIC"],
    "NT": ["WA", "SA", "QLD"],
    "WA": ["SA", "NT"]
}  # fill in with adjacent states for each state!


class FictionalAnimal:
    '''
    Represents a fictional Australian animal used in the relocation simulation.

    Each animal has a name, habitat, threat, and current state.
    '''
    def __init__(self, name: str, habitat: str, threat: str):
        '''
        Initialises a new FictionalAnimal with the given name, habitat, and threat.
        Sets the starting state to 'ACT' by default.

        Parameters:
            name (str): The name of the animal.
            habitat (str): The animal's preferred habitat.
            threat (str): The name of another animal that poses a threat.
        '''
        self.name = name
        self.habitat = habitat
        self.threat = threat
        self.state = 'ACT'  # Canberra, the capital, as default


    def get_state(self) -> str:
        '''Returns the current state where this animal is located.'''
        return self.state


    def set_state(self, state: str):
        '''
        Updates the animal's state if the new state is valid.

        A valid state is one that exists in the list of defined states.
        If the state is not valid, the location does not change.

        Parameters:
            state (str): The new state to assign to the animal.
        '''
        if state in ADJACENT_STATES.keys() or state == 'ACT':
            self.state = state
        # else: ignore invalid state


    def __str__(self) -> str:
        '''
        Returns a formatted string representing the animal's details.
        Format:
        <name>
           Habitat : <habitat>
           Threat  : <threat>
           State   : <state>
        '''
        return (f"{self.name}\n"
                f"   Habitat : {self.habitat}\n"
                f"   Threat  : {self.threat}\n"
                f"   State   : {self.state}")


    def load_dataset() -> list['FictionalAnimal']:
        '''
        Loads animal data from animals.csv and returns a list of FictionalAnimal
        objects.

        Lines must follow the format: <name>,<habitat>,<threat>

        Lines with missing or extra fields are skipped.
        If the file does not exist, returns an empty list.

        Returns:
            list[FictionalAnimal]: A list of valid animal objects.
        '''
        animals = []
        try:
            with open('animals.csv', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        name, habitat, threat = parts
                        animals.append(FictionalAnimal(name, habitat, threat))
        except FileNotFoundError:
            return []
        return animals


def relocate_animals(animals: list[FictionalAnimal]):
    '''
    Simulates the relocation of Australian animals. 
    
    No two animals can share the same state, and no animal can be next to its
    threat.

    The relocation respects the following fixed state order:
    NSW → QLD → VIC → TAS → SA → NT → WA

    Animals are considered for relocation one by one, in the order they appear
    in the list. If an animal cannot be placed in a state, its state remains 
    as 'ACT'.

    Parameters:
        animals (list[FictionalAnimal]): A list of FictionalAnimal objects.
    '''
    state_order = ["NSW", "QLD", "VIC", "TAS", "SA", "NT", "WA"]
    occupied = {}  # state -> animal name mapping

    for animal in animals:
        placed = False  # track if this animal found a safe state

        for state in state_order:
            # skip if already occupied
            if state in occupied:
                continue

            # check if this state is safe
            safe = True

            # find the threat animal (if it exists)
            threat_animal = next((a for a in animals if a.name == animal.threat), None)

            # (1) Cannot be placed in the same state as its threat
            if threat_animal and threat_animal.get_state() == state:
                safe = False

            # (2) Cannot be placed next to its threat (adjacent state check)
            elif threat_animal and threat_animal.get_state() in ADJACENT_STATES.get(state, []):
                safe = False

            # (3) Cannot be a threat to any animal in adjacent states
            else:
                for adj_state in ADJACENT_STATES[state]:
                    if adj_state in occupied:
                        adj_animal_name = occupied[adj_state]
                        adj_animal = next((a for a in animals if a.name == adj_animal_name), None)
                        if adj_animal and adj_animal.threat == animal.name:
                            safe = False
                            break

            # if all checks pass, place the animal
            if safe:
                animal.set_state(state)
                occupied[state] = animal.name
                placed = True
                break

        # if no safe state found → remains in 'ACT' (default)
        if not placed:
            animal.set_state('ACT')


def main():
    '''
    Runs the full relocation simulation from start to finish.

    This function should:
    - Load the fictional animal data from animals.txt
    - Print each animal's details before relocation
    - Relocate the animals using relocate_animals()
    - Print each animal's updated details after relocation
    '''
    print(">> READING IN ANIMALS.")
    animals = FictionalAnimal.load_dataset()
    print(f"Loaded {len(animals)} animals from animals.csv.\n")
    print(">> BEFORE RELOCATION.")
    for i, a in enumerate(animals):
        if i > 0:           
            print()
        print(a)
    print()                 
    print(">> RELOCATING ANIMALS.")
    relocate_animals(animals)
    relocated_count = sum(1 for a in animals if a.get_state() != 'ACT')
    print(f"Animals relocated: {relocated_count}/{len(animals)}\n")
    print(">> SUMMARY.")
    for a in animals:
        print(f"{a.name}: {a.get_state()}")


# Do not modify this!
if __name__ == '__main__':
    main()
