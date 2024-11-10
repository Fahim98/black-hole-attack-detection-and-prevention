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
        self.color = (0, 255, 0) if not is_malicious else (255, 165, 0)
        self.size = 15
        self.reputation = 1.0
        self.energy = 100
        self.packets_forwarded = 0
        self.packets_dropped = 0
        self.suspicious_score = 0
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        self.connections = []
        self.node_type = "Normal" if not is_malicious else "Potential Black Hole"

class BlackHoleDetectionSimulation:
    def __init__(self, width=1400, height=900):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Interactive Black Hole Detection Simulation")
        
        self.COLORS = {
            'BACKGROUND': (20, 20, 40),
            'NODE_NORMAL': (0, 255, 0),
            'NODE_MALICIOUS': (255, 165, 0),
            'NODE_DETECTED': (255, 0, 0),
            'CONNECTION': (100, 100, 100),
            'TEXT': (255, 255, 255),
            'PACKET': (255, 255, 255)
        }
        
        self.width = width
        self.height = height
        self.num_nodes = 30
        self.malicious_ratio = 0.2
        
        self.nodes = []
        self.packets = []
        self.detected_nodes = set()
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.selected_node = None
        self.font = pygame.font.Font(None, 24)
        
        self.create_network()
    
    def create_network(self):
        num_malicious = int(self.num_nodes * self.malicious_ratio)
        for i in range(self.num_nodes):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            is_malicious = i < num_malicious
            node = NetworkNode(x, y, i, is_malicious)
            self.nodes.append(node)
        self.create_network_connections()
    
    def create_network_connections(self):
        for node in self.nodes:
            potential_connections = [
                other for other in self.nodes 
                if other != node and 
                math.sqrt((node.x - other.x)**2 + (node.y - other.y)**2) < 200
            ]
            node.connections = sorted(
                potential_connections, 
                key=lambda x: math.sqrt((node.x - x.x)**2 + (node.y - x.y)**2)
            )[:4]
    
    def generate_packet(self):
        if random.random() < 0.1:
            source = random.choice(self.nodes)
            destination = random.choice([node for node in self.nodes if node != source])
            packet = Packet(source, destination)
            if source.is_malicious and random.random() < 0.5:
                packet.is_intercepted = True
                packet.color = (255, 0, 0)
            self.packets.append(packet)
    
    def update_packets(self):
        for packet in self.packets[:]:
            dx = packet.destination.x - packet.position[0]
            dy = packet.destination.y - packet.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 5:
                packet.position[0] += dx * 0.02
                packet.position[1] += dy * 0.02
            else:
                if packet.is_intercepted:
                    packet.source.suspicious_score += 1
                self.packets.remove(packet)
    
    def detect_black_hole_nodes(self):
        for node in self.nodes:
            if node.is_malicious:
                if (node.suspicious_score > 10 or 
                    node.packets_dropped / max(node.packets_forwarded, 1) > 0.5):
                    node.color = self.COLORS['NODE_DETECTED']
                    node.node_type = "Confirmed Black Hole"
                    self.detected_nodes.add(node.id)
    
    def render_network(self):
        self.screen.fill(self.COLORS['BACKGROUND'])
        
        for node in self.nodes:
            for connected_node in node.connections:
                pygame.draw.line(self.screen, self.COLORS['CONNECTION'], (node.x, node.y), (connected_node.x, connected_node.y), 1)
        
        for node in self.nodes:
            pygame.draw.circle(self.screen, node.color, (int(node.x), int(node.y)), node.size)
            if self.selected_node == node.id:
                self.display_node_details(node)
        
        for packet in self.packets:
            pygame.draw.circle(self.screen, packet.color, (int(packet.position[0]), int(packet.position[1])), 5)
        
        stats = [
            f"Total Nodes: {self.num_nodes}",
            f"Malicious Nodes: {int(self.num_nodes * self.malicious_ratio)}",
            f"Detected Black Holes: {len(self.detected_nodes)}",
            f"Active Packets: {len(self.packets)}",
            f"Status: {'Paused' if self.paused else 'Running'}"
        ]
        
        for i, text in enumerate(stats):
            text_surface = self.font.render(text, True, self.COLORS['TEXT'])
            self.screen.blit(text_surface, (10, 10 + i * 25))
    
    def display_node_details(self, node):
        details = [
            f"Node ID: {node.id}",
            f"Type: {node.node_type}",
            f"Reputation: {node.reputation:.2f}",
            f"Energy: {node.energy}",
            f"Suspicious Score: {node.suspicious_score}",
            f"Packets Forwarded: {node.packets_forwarded}",
            f"Packets Dropped: {node.packets_dropped}"
        ]
        
        for i, detail in enumerate(details):
            text_surface = self.font.render(detail, True, self.COLORS['TEXT'])
            self.screen.blit(text_surface, (self.width - 200, 10 + i * 20))
    
    def handle_click(self, pos):
        for node in self.nodes:
            distance = math.sqrt((pos[0] - node.x)**2 + (pos[1] - node.y)**2)
            if distance < node.size:
                self.selected_node = node.id if self.selected_node != node.id else None
                node.is_malicious = not node.is_malicious
                node.color = self.COLORS['NODE_MALICIOUS'] if node.is_malicious else self.COLORS['NODE_NORMAL']
    
    def run_simulation(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            
            if not self.paused:
                self.generate_packet()
                self.update_packets()
                self.detect_black_hole_nodes()
                self.render_network()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    random.seed(42)
    np.random.seed(42)
    simulation = BlackHoleDetectionSimulation(width=1400, height=900)
    simulation.run_simulation()

if __name__ == "__main__":
    main()
