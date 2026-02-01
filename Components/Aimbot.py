import math
from components.base import BaseComponent
from utils.game import get_entities, get_player_position, get_camera_angle, set_camera_angle, is_entity_in_fov, get_entity_position
from utils.render import draw_circle

class Aimbot(BaseComponent):
    def __init__(self):
        super().__init__("Aimbot")
        self.enabled = False
        self.fov_radius = 100
        self.smoothness = 0.5
        self.silent_aim = True
        self.target = None
        
    def update(self):
        if not self.enabled:
            return
            
        # Find target within FOV
        self.target = self.find_target_in_fov()
        
        if self.target:
            # Calculate smooth movement towards target
            current_angle = get_camera_angle()
            target_pos = get_entity_position(self.target)
            player_pos = get_player_position()
            
            # Calculate angle to target
            dx = target_pos[0] - player_pos[0]
            dy = target_pos[1] - player_pos[1]
            dz = target_pos[2] - player_pos[2]
            
            target_angle = [math.atan2(dy, dx), math.atan2(dz, math.sqrt(dx*dx + dy*dy))]
            
            # Apply smoothing
            smoothed_angle = [
                current_angle[0] * (1-self.smoothness) + target_angle[0] * self.smoothness,
                current_angle[1] * (1-self.smoothness) + target_angle[1] * self.smoothness
            ]
            
            # Update camera angle
            set_camera_angle(smoothed_angle)
            
            # Hide crosshair in silent aim mode
            if self.silent_aim:
                # Crosshair hiding logic would go here
                pass
                
    def find_target_in_fov(self):
        # Get all entities in the game world
        entities = get_entities()
        
        # Filter for players/enemies within FOV
        valid_targets = []
        for entity in entities:
            # Check if entity is in FOV cone
            if is_entity_in_fov(entity):
                valid_targets.append(entity)
        
        # Return closest valid target
        if not valid_targets:
            return None
            
        return min(valid_targets, key=lambda x: get_distance_to_entity(get_player_position(), get_entity_position(x)))
    
    def render(self):
        if self.enabled and self.target:
            # Draw FOV circle
            draw_circle(
                get_entity_position(self.target),
                self.fov_radius,
                color=(0, 255, 0, 100)  # Semi-transparent green
            )
