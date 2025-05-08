import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
import base64
from typing import List, Dict, Optional
from dataclasses import dataclass
from trilateration import Point, TrilaterationSolver

@dataclass
class VisualizationConfig:
    figure_size: tuple = (10, 8)
    dpi: int = 100
    marker_size: int = 100
    history_line_width: float = 2.0
    update_interval: int = 1000  # milliseconds
    show_grid: bool = True
    show_legend: bool = True
    show_confidence: bool = True

class PositionVisualizer:
    def __init__(self, trilateration_solver: TrilaterationSolver, config: Optional[VisualizationConfig] = None):
        self.solver = trilateration_solver
        self.config = config or VisualizationConfig()
        self.fig = None
        self.ax = None
        self.scatter = None
        self.history_line = None
        self.landmark_scatter = None
        self.animation = None
        
    def _setup_plot(self):
        """Initialize the plot with proper styling"""
        plt.style.use('seaborn')
        self.fig, self.ax = plt.subplots(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Set up the plot
        self.ax.set_title('Real-time Position Tracking')
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        
        if self.config.show_grid:
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
        # Initialize scatter plots
        self.scatter = self.ax.scatter([], [], c='blue', s=self.config.marker_size, 
                                     label='Current Position', alpha=0.8)
        self.history_line, = self.ax.plot([], [], 'b--', linewidth=self.config.history_line_width,
                                        label='Position History', alpha=0.5)
        self.landmark_scatter = self.ax.scatter([], [], c='red', s=self.config.marker_size,
                                              label='Landmarks', alpha=0.6)
        
        if self.config.show_legend:
            self.ax.legend()
            
        # Set equal aspect ratio
        self.ax.set_aspect('equal')
        
    def _update_plot(self, frame):
        """Update the plot with current position and landmarks"""
        # Get current position and history
        history = self.solver.get_position_history()
        landmarks = self.solver.landmark_positions
        
        if not history:
            return self.scatter, self.history_line, self.landmark_scatter
            
        # Update current position
        current_pos = history[-1]
        self.scatter.set_offsets([[current_pos.x, current_pos.y]])
        
        # Update history line
        if len(history) > 1:
            x_coords = [p.x for p in history]
            y_coords = [p.y for p in history]
            self.history_line.set_data(x_coords, y_coords)
            
        # Update landmarks
        if landmarks:
            landmark_x = [p.x for p in landmarks.values()]
            landmark_y = [p.y for p in landmarks.values()]
            self.landmark_scatter.set_offsets(np.column_stack([landmark_x, landmark_y]))
            
        # Adjust plot limits
        self._adjust_plot_limits()
        
        return self.scatter, self.history_line, self.landmark_scatter
        
    def _adjust_plot_limits(self):
        """Adjust plot limits to show all points with padding"""
        history = self.solver.get_position_history()
        landmarks = self.solver.landmark_positions
        
        if not history and not landmarks:
            return
            
        # Get all x and y coordinates
        x_coords = [p.x for p in history] + [p.x for p in landmarks.values()]
        y_coords = [p.y for p in history] + [p.y for p in landmarks.values()]
        
        if not x_coords or not y_coords:
            return
            
        # Calculate limits with padding
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        x_padding = (x_max - x_min) * 0.1
        y_padding = (y_max - y_min) * 0.1
        
        self.ax.set_xlim(x_min - x_padding, x_max + x_padding)
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)
        
    def start_visualization(self):
        """Start real-time visualization"""
        self._setup_plot()
        self.animation = FuncAnimation(
            self.fig,
            self._update_plot,
            interval=self.config.update_interval,
            blit=True
        )
        plt.show()
        
    def get_current_plot(self) -> str:
        """Get current plot as base64 encoded image"""
        if self.fig is None:
            self._setup_plot()
            
        # Update the plot
        self._update_plot(None)
        
        # Save plot to buffer
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', dpi=self.config.dpi, bbox_inches='tight')
        buf.seek(0)
        
        # Convert to base64
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"
        
    def close(self):
        """Close the visualization"""
        if self.animation is not None:
            self.animation.event_source.stop()
        if self.fig is not None:
            plt.close(self.fig) 