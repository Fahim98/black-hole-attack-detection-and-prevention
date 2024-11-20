import pygame
import random
import pandas as pd

# Load the dataset
file_path = "black_hole_detection_data.csv"  # Replace with the correct path to your file
data = pd.read_csv(file_path)

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NODE_RADIUS = 10
FONT_SIZE = 16
FPS = 60
MAX_NODES = 50  # Reduced for better clarity during animations
PACKET_SPEED = 2  # Speed of moving packets
TRUST_THRESHOLD_SUSPICIOUS = 0.4
TRUST_THRESHOLD_BLACK_HOLE = 0.2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic AODV Black Hole Attack Simulation")
font = pygame.font.Font(None, FONT_SIZE)

# Randomly select a subset of nodes for display
sampled_data = data.sample(n=MAX_NODES)
nodes = []
for _, row in sampled_data.iterrows():
    nodes.append({
        "id": row["Node_ID"],
        "type": row["Node_Type"],
        "trust_value": random.uniform(0.0, 1.0),  # Randomized trust values for variability
        "detection_confidence": random.uniform(0.0, 1.0),  # Randomized detection confidence
        "energy": random.uniform(50.0, 100.0),  # Randomized energy levels
        "position": [random.randint(NODE_RADIUS, SCREEN_WIDTH - NODE_RADIUS),
                     random.randint(NODE_RADIUS, SCREEN_HEIGHT - NODE_RADIUS)],
        "velocity": [random.choice([-1, 1]) * random.random() * 2,
                     random.choice([-1, 1]) * random.random() * 2],
        "packets_forwarded": 0,
        "packets_dropped": 0,
    })

# Packet data for animation
packets = []

# Helper Functions
def spawn_packet(source, target):
    """Create a new packet traveling between two nodes."""
    packets.append({
        "source": source,
        "target": target,
        "position": source["position"][:],
        "color": BLUE if source["type"] != "Confirmed Black Hole" else RED
    })

def update_node_type(node):
    """Update the type of a node based on its trust value."""
    if node["trust_value"] < TRUST_THRESHOLD_BLACK_HOLE:
        node["type"] = "Confirmed Black Hole"
    elif node["trust_value"] < TRUST_THRESHOLD_SUSPICIOUS:
        node["type"] = "Suspicious"
    else:
        node["type"] = "Normal"

def draw_nodes(selected_node=None):
    """Draw nodes dynamically based on their type and optionally highlight a selected node."""
    for node in nodes:
        update_node_type(node)
        if selected_node and node == selected_node:
            color = (0, 128, 255)  # Highlight color for the selected node
        else:
            color = GREEN if node["type"] == "Normal" else YELLOW if node["type"] == "Suspicious" else RED
        pygame.draw.circle(screen, color, node["position"], NODE_RADIUS)

def display_node_details(node, position):
    """Display detailed information about a node."""
    details = [
        f"ID: {node['id']}",
        f"Type: {node['type']}",
        f"Trust Value: {node['trust_value']:.2f}",
        f"Detection Confidence: {node['detection_confidence']:.2f}",
        f"Energy: {node['energy']:.2f}",
        f"Packets Forwarded: {node['packets_forwarded']}",
        f"Packets Dropped: {node['packets_dropped']}"
    ]
    x, y = position
    pygame.draw.rect(screen, WHITE, (x - 10, y - 10, 200, len(details) * FONT_SIZE + 20))  # Background
    pygame.draw.rect(screen, BLACK, (x - 10, y - 10, 200, len(details) * FONT_SIZE + 20), 2)  # Border
    for i, line in enumerate(details):
        text = font.render(line, True, BLACK)
        screen.blit(text, (x, y + i * FONT_SIZE))

def draw_packets():
    """Draw packets."""
    for packet in packets:
        pygame.draw.circle(screen, packet["color"], (int(packet["position"][0]), int(packet["position"][1])), 5)

def move_packets():
    """Move packets and update node metrics."""
    global packets
    for packet in packets[:]:
        source_pos = packet["source"]["position"]
        target_pos = packet["target"]["position"]
        dx = target_pos[0] - packet["position"][0]
        dy = target_pos[1] - packet["position"][1]
        dist = (dx**2 + dy**2)**0.5
        if dist > PACKET_SPEED:
            packet["position"][0] += PACKET_SPEED * dx / dist
            packet["position"][1] += PACKET_SPEED * dy / dist
        else:
            # Packet reached target
            packet["target"]["packets_forwarded"] += 1
            packet["source"]["trust_value"] -= 0.01  # Degrade trust for dropped packets
            packets.remove(packet)

def move_nodes():
    """Move nodes randomly on the screen."""
    for node in nodes:
        for i in range(2):  # Update x and y positions
            node["position"][i] += node["velocity"][i]
            if node["position"][i] < NODE_RADIUS or node["position"][i] > (SCREEN_WIDTH if i == 0 else SCREEN_HEIGHT) - NODE_RADIUS:
                node["velocity"][i] *= -1  # Reverse direction

def draw_legend():
    """Draw a legend for the simulation."""
    legend_items = [
        ("Normal", GREEN),
        ("Suspicious", YELLOW),
        ("Confirmed Black Hole", RED),
        ("Packet (Forwarded)", BLUE),
        ("Packet (Dropped)", RED),
    ]
    x, y = SCREEN_WIDTH - 150, 10
    for label, color in legend_items:
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 20, y - NODE_RADIUS // 2))
        y += 30

def count_black_holes():
    """Count the number of confirmed black holes."""
    return sum(1 for node in nodes if node["type"] == "Confirmed Black Hole")

# Main simulation loop
running = True
clock = pygame.time.Clock()
selected_node = None
SPAWN_INTERVAL = 50  # Frames
spawn_counter = 0

while running:
    screen.fill(WHITE)
    draw_nodes(selected_node)
    draw_packets()
    draw_legend()

    # Display black hole count
    black_hole_count = count_black_holes()
    text = font.render(f"Black Holes Detected: {black_hole_count}", True, BLACK)
    screen.blit(text, (10, SCREEN_HEIGHT - 30))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for node in nodes:
                node_pos = node["position"]
                distance = ((pos[0] - node_pos[0]) ** 2 + (pos[1] - node_pos[1]) ** 2) ** 0.5
                if distance <= NODE_RADIUS:
                    selected_node = None if node == selected_node else node
                    break

    # Move and update packets and nodes
    move_packets()
    move_nodes()

    # Periodically spawn packets
    spawn_counter += 1
    if spawn_counter >= SPAWN_INTERVAL:
        spawn_counter = 0
        if len(nodes) > 1:
            source, target = random.sample(nodes, 2)
            spawn_packet(source, target)

    # Display node details if one is selected
    if selected_node:
        display_node_details(selected_node, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
