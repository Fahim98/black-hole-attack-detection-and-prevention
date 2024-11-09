import pygame
import random
import math
import numpy as np

class Packet:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.position = [source.x, source.y]
        self.progress = 0
        self.color = (255, 255, 255)  # White packet
        self.is_intercepted = False

class NetworkNode:
    def __init__(self, x, y, node_id, is_malicious=False):
        self.x = x
        self.y = y
        self.id = node_id
        self.is_malicious = is_malicious
        
        # Enhanced node characteristics
        self.color = (0, 255, 0) if not is_malicious else (255, 165, 0)
        self.size = 15
        
        # Advanced network metrics
        self.reputation = 1.0
        self.energy = 100
        self.packets_forwarded = 0
        self.packets_dropped = 0
        self.suspicious_score = 0
        
        # Dynamic movement
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        
        # Connection management
        self.connections = []
        
        # Detailed node information
        self.node_type = "Normal" if not is_malicious else "Potential Black Hole"

class BlackHoleDetectionSimulation:
    def __init__(self, width=1400, height=900):
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Advanced Black Hole Attack Detection Simulation")
        
        # Color palette
        self.COLORS = {
            'BACKGROUND': (20, 20, 40),
            'NODE_NORMAL': (0, 255, 0),
            'NODE_MALICIOUS': (255, 165, 0),
            'NODE_DETECTED': (255, 0, 0),
            'CONNECTION': (100, 100, 100),
            'TEXT': (255, 255, 255),
            'PACKET': (255, 255, 255)
        }
        
        # Simulation parameters
        self.width = width
        self.height = height
        self.num_nodes = 50
        self.malicious_ratio = 0.2
        
        # Simulation components
        self.nodes = []
        self.packets = []
        self.detected_nodes = set()
        
        # Simulation control
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        
        # Create network
        self.create_network()
    
    def create_network(self):
        """Generate a sophisticated network topology"""
        num_malicious = int(self.num_nodes * self.malicious_ratio)
        
        # Create nodes with strategic positioning
        for i in range(self.num_nodes):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            
            is_malicious = i < num_malicious
            node = NetworkNode(x, y, i, is_malicious)
            self.nodes.append(node)
        
        # Establish network connections
        self.create_network_connections()
    
    def create_network_connections(self):
        """Create intelligent network connections"""
        for node in self.nodes:
            # Find potential connections
            potential_connections = [
                other for other in self.nodes 
                if other != node and 
                math.sqrt((node.x - other.x)**2 + (node.y - other.y)**2) < 200
            ]
            
            # Limit and prioritize connections
            node.connections = sorted(
                potential_connections, 
                key=lambda x: math.sqrt((node.x - x.x)**2 + (node.y - x.y)**2)
            )[:4]
    
    def generate_packet(self):
        """Dynamically generate network packets"""
        if random.random() < 0.1:  # Packet generation probability
            source = random.choice(self.nodes)
            
            # Intelligent destination selection
            destination = random.choice([
                node for node in self.nodes 
                if node != source and node not in source.connections
            ])
            
            packet = Packet(source, destination)
            
            # Malicious node packet interception
            if source.is_malicious and random.random() < 0.5:
                packet.is_intercepted = True
                packet.color = (255, 0, 0)  # Red for intercepted
            
            self.packets.append(packet)
    
    def update_packets(self):
        """Advanced packet transmission simulation"""
        for packet in self.packets[:]:
            # Calculate movement towards destination
            dx = packet.destination.x - packet.position[0]
            dy = packet.destination.y - packet.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            # Move packet
            if distance > 5:
                packet.progress += 0.02
                packet.position[0] += dx * 0.02
                packet.position[1] += dy * 0.02
            else:
                # Packet reached destination
                if packet.is_intercepted:
                    packet.source.suspicious_score += 1
                
                self.packets.remove(packet)
    
    def detect_black_hole_nodes(self):
        """Sophisticated black hole detection mechanism"""
        for node in self.nodes:
            if node.is_malicious:
                # Detection based on multiple metrics
                if (node.suspicious_score > 10 or 
                    node.packets_dropped / max(node.packets_forwarded, 1) > 0.5):
                    
                    node.color = self.COLORS['NODE_DETECTED']
                    node.node_type = "Confirmed Black Hole"
                    self.detected_nodes.add(node.id)
    
    def render_network(self):
        """Comprehensive network visualization"""
        # Clear screen
        self.screen.fill(self.COLORS['BACKGROUND'])
        
        # Render network connections
        for node in self.nodes:
            for connected_node in node.connections:
                pygame.draw.line(
                    self.screen, 
                    self.COLORS['CONNECTION'], 
                    (node.x, node.y), 
                    (connected_node.x, connected_node.y), 
                    1
                )
        
        # Render nodes
        for node in self.nodes:
            pygame.draw.circle(
                self.screen, 
                node.color, 
                (int(node.x), int(node.y)), 
                node.size
            )
        
        # Render packets
        for packet in self.packets:
            pygame.draw.circle(
                self.screen,
                packet.color,
                (int(packet.position[0]), int(packet.position[1])),
                5
            )
        
        # Render detailed statistics
        stats = [
            f"Total Nodes: {self.num_nodes}",
            f"Malicious Nodes: {int(self.num_nodes * self.malicious_ratio)}",
            f"Detected Black Holes: {len(self.detected_nodes)}",
            f"Active Packets: {len(self.packets)}",
            f"Status: {'Paused' if self.paused else 'Running'}"
        ]
        
        for i, text in enumerate(stats):
            text_surface = self.font.render(text, True, self.COLORS['TEXT'])
            self.screen.blit(text_surface, (10, 10 + i*25))
    
    def run_simulation(self):
        """Main simulation loop"""
        while self.running:
            # # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
            
            if not self.paused:
                self.generate_packet()
                self.update_packets()
                self.detect_black_hole_nodes()
                self.render_network()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(60)
        
        # Cleanup
        pygame.quit()

def main():
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Create and run the advanced simulation
    simulation = BlackHoleDetectionSimulation(
        width=1400, 
        height=900
    )
    simulation.run_simulation()

# Execute simulation
if __name__ == "__main__":
    main()