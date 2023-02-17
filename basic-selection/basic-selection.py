"""
Basic demonstration of natural selection.

In this simulation, agents are born with a random chance of winning a challenge
for food, and a random amount of energy gained from winning. They also have a
random chance of reproducing each frame.

The agents' stats decay over time, and they will die if they run out of energy
or health. They will also die of old age after a certain number of frames.
"""

import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Constants
DESCRIPTION = "Basic Selection"
OLD_AGE = 1000
REPRODUCE_AGE = 300
REPRODUCE_CHANCE = 0.002

STAT_DECAY_RATE = 0.01
CRITICAL_ENERGY = 0.1  # Must be less than 0.5
MAX_WIN_CHANCE = 0.3
MAX_ENERGY_GAIN = 0.2
MUTATION_RATE = 0.003

NUM_INIT_AGENTS = 10
MAX_FOOD_PELLETS = 5
NUM_FRAMES = 100000


class Agent:
    """
    Represents an agent in the simulated world.

    Has a unique numerical ID, age (# of frames), health, and energy.
    """
    agent_id = 0
    
    def __init__(self):
        self.id = Agent.agent_id
        Agent.agent_id += 1
        self.age = 0
        self.health = 0.5
        self.energy = 0.5
    
    def __repr__(self):
        hp = round(self.health*100)
        en = round(self.energy*100)
        return f"Agent(#{self.id}, Age={self.age}, HP={hp}, EN={en})"
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = max(0, value)

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = max(0, min(1, value))
    
    @property
    def energy(self):
        return self._energy
    
    @energy.setter
    def energy(self, value):
        self._energy = max(0, min(1, value))
    
    def tick(self):
        """
        Updates the agent for this tick.
        """
        self.age += 1
        self.energy -= STAT_DECAY_RATE
        if self.energy < CRITICAL_ENERGY:
            self.health -= STAT_DECAY_RATE
        elif self.energy > 1-CRITICAL_ENERGY:
            self.health += STAT_DECAY_RATE


class Agent(Agent):
    """
    From this point on, the agent cannot control its own stats.
    It can only try its best to survive in the env.
    """
    def __init__(self):
        super().__init__()
        self.win_chance = random.random() * MAX_WIN_CHANCE
        self.energy_gain = random.random() * MAX_ENERGY_GAIN

    def challenge(self) -> bool:
        # Variable chance of losing
        if random.random() < 1-self.win_chance:
            return False
        # Only eat if we need the energy
        if self.energy < 1-self.energy_gain:
            return True
        else:
            return False
    
    def reproduce(self) -> Agent:
        # Mimic chances of the parent, with some mutation
        def mutate(value, abs_delta):
            return max(0, value + random.random()*(abs_delta*2) - abs_delta)
        new_agent = Agent()
        new_agent.win_chance = min(mutate(self.win_chance, MUTATION_RATE), MAX_WIN_CHANCE)
        new_agent.energy_gain = min(mutate(self.energy_gain, MUTATION_RATE), MAX_ENERGY_GAIN)
        return new_agent


class Env:
    """
    Represents the environment in which the agents live.
    """

    def __init__(self):
        self.frame = 0
        self.food_count = 0
        self.agents = []
    
    def __repr__(self):
        return f"Env(Frame {self.frame}, {len(self.agents)} agents, {self.food_count} food)"
    
    def add_agent(self, agent: Agent):
        self.agents.append(agent)
    
    def remove_agent(self, agent: Agent):
        self.agents.remove(agent)
    
    def tick(self):
        """
        Updates the environment for this tick.
        """
        self.frame += 1

        # Randomly order the agents, then have them challenge for food
        random.shuffle(self.agents)
        for agent in self.agents:
            if self.food_count > 0 and agent.challenge():
                agent.energy += agent.energy_gain
                self.food_count -= 1

        # Track the agents that survived this tick
        self.next_agents = []
        for agent in self.agents:
            agent.tick()
            # No health
            if agent.health <= 0:
                # print(f"Agent #{agent.id} starved to death")
                continue
            # Old age
            if random.random() <= (agent.age-OLD_AGE) / (OLD_AGE*10):
                # print(f"Agent #{agent.id} died of old age")
                continue
            # Reproduce?
            if agent.age >= REPRODUCE_AGE and random.random() < REPRODUCE_CHANCE:
                # print(f"Agent #{agent.id} reproduced")
                self.next_agents.append(agent.reproduce())
            self.next_agents.append(agent)
        
        # Update the list of agents
        self.agents = self.next_agents


def run_env():
    # Initial setup
    Agent.agent_id = 0
    env = Env()
    for _ in range(NUM_INIT_AGENTS):
        env.add_agent(Agent())
    
    # Main loop
    hist_num_agents = []
    hist_avg_win_chance = []
    hist_avg_energy_gain = []
    hist_avg_expected = []
    for _ in range(NUM_FRAMES):
        hist_num_agents.append(len(env.agents))
        if not env.agents:
            hist_avg_win_chance.append(0)
            hist_avg_energy_gain.append(0)
            hist_avg_expected.append(0)
            break
        hist_avg_win_chance.append(sum([a.win_chance for a in env.agents]) / len(env.agents))
        hist_avg_energy_gain.append(sum([a.energy_gain for a in env.agents]) / len(env.agents))
        hist_avg_expected.append(sum([a.win_chance*a.energy_gain for a in env.agents])
                                 / len(env.agents))
        if env.frame % 10000 == 0:
            print(env)

        # Add food pellets
        env.food_count += random.randint(0, MAX_FOOD_PELLETS - env.food_count)
        env.tick()
    
    print("Done!")
    print(f"Total # of agents created: {Agent.agent_id}")
    average_age = sum([a.age for a in env.agents]) / (len(env.agents) or 1)
    print(f"Average age of agents: {round(average_age)} frames")
    
    return hist_num_agents, hist_avg_win_chance, hist_avg_energy_gain, hist_avg_expected


def plot_results(hist_num_agents, hist_avg_win_chance, hist_avg_energy_gain, hist_avg_expected, batch_expected):
    # Plot the results
    gs = gridspec.GridSpec(2, 2)
    plt.figure()

    # Record all coonstant values
    plt.subplot(gs[:, 0])
    plt.grid(False)
    plt.axis("off")
    plt.text(0, 0.5, f"""
Natural Selection Demo
{DESCRIPTION}

OLD_AGE = {OLD_AGE}
REPRODUCE_AGE = {REPRODUCE_AGE}
REPRODUCE_CHANCE = {REPRODUCE_CHANCE}

STAT_DECAY_RATE = {STAT_DECAY_RATE}
CRITICAL_ENERGY = {CRITICAL_ENERGY}
MAX_WIN_CHANCE = {MAX_WIN_CHANCE}
MAX_ENERGY_GAIN = {MAX_ENERGY_GAIN}
MUTATION_RATE = {MUTATION_RATE}

NUM_INIT_AGENTS = {NUM_INIT_AGENTS}
MAX_FOOD_PELLETS = {MAX_FOOD_PELLETS}
NUM_FRAMES = {NUM_FRAMES}
""", verticalalignment="center", bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Plot 1
    plt.subplot(gs[0, 1])
    plt.plot(hist_avg_expected, color="tab:green", label="Expected energy gain")
    plt.xlabel("Frame")
    plt.ylim(0, max(hist_avg_expected)*1.1)
    plt.legend()

    # Plot 2
    plt.subplot(gs[1, 1])
    plt.plot(hist_avg_win_chance, label="Average win chance")
    plt.plot(hist_avg_energy_gain, label="Average energy gain")
    plt.xlabel("Frame")
    plt.ylim(0, max(hist_avg_win_chance + hist_avg_energy_gain)*1.1)
    plt.legend()

    # Plot 3
    # plt.subplot(gs[:, 2])
    # plt.plot(batch_expected)
    # plt.xlabel("Trial")
    # plt.ylabel("Final expected energy gain")
    # plt.ylim(0, max(batch_expected)*1.1)

    # Show plots
    plt.savefig(f"{DESCRIPTION}.png", bbox_inches="tight")
    plt.show()
    

def main():
    hist_num_agents, hist_avg_win_chance, hist_avg_energy_gain, hist_avg_expected = run_env()
    plot_results(hist_num_agents, hist_avg_win_chance, hist_avg_energy_gain, hist_avg_expected, None)


if __name__ == "__main__":
    main()
