"""
Custom styling utilities for the ProshivkaTool GUI
"""
import tkinter as tk
from tkinter import ttk

class ModernStyle:
    """Modern styling configuration for tkinter widgets"""
    
    # Color scheme
    COLORS = {
        'primary': '#4facfe',
        'secondary': '#00f2fe',
        'background': '#1a1a2e',
        'surface': '#2e2e3e',
        'accent': '#e74c3c',
        'text_primary': '#ffffff',
        'text_secondary': '#e0e0e0',
        'text_muted': '#a0a0a0',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'error': '#e74c3c'
    }
    
    @classmethod
    def apply_modern_style(cls, style):
        """Apply modern styling to ttk.Style object"""
        
        # Configure button styles
        style.configure('Modern.TButton',
                       foreground=cls.COLORS['text_primary'],
                       background=cls.COLORS['primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10),
                       padding=(15, 8))
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['secondary']),
                           ('pressed', cls.COLORS['accent'])])
        
        # Configure label styles
        style.configure('Modern.TLabel',
                       foreground=cls.COLORS['text_primary'],
                       background=cls.COLORS['background'],
                       font=('Arial', 10))
        
        style.configure('Title.TLabel',
                       foreground=cls.COLORS['text_primary'],
                       background=cls.COLORS['background'],
                       font=('Arial', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       foreground=cls.COLORS['text_secondary'],
                       background=cls.COLORS['background'],
                       font=('Arial', 12))
        
        # Configure frame styles
        style.configure('Modern.TFrame',
                       background=cls.COLORS['surface'],
                       borderwidth=1,
                       relief='solid')
        
        # Configure progressbar
        style.configure('Modern.TProgressbar',
                       background=cls.COLORS['primary'],
                       troughcolor=cls.COLORS['surface'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'])
        
        # Configure scale
        style.configure('Modern.TScale',
                       background=cls.COLORS['surface'],
                       troughcolor=cls.COLORS['background'],
                       borderwidth=0,
                       sliderlength=20,
                       sliderrelief='flat')
        
        return style

class GradientFrame(tk.Frame):
    """Custom frame widget with gradient background"""
    
    def __init__(self, parent, color1="#4facfe", color2="#00f2fe", **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind('<Configure>', self._on_configure)
        
    def _on_configure(self, event=None):
        """Handle widget resize to redraw gradient"""
        self._draw_gradient()
        
    def _draw_gradient(self):
        """Draw gradient background"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Create canvas for gradient
        if hasattr(self, '_gradient_canvas'):
            self._gradient_canvas.destroy()
            
        self._gradient_canvas = tk.Canvas(self, width=width, height=height)
        self._gradient_canvas.place(x=0, y=0)
        
        # Draw gradient
        self._create_gradient(self._gradient_canvas, width, height)
        
    def _create_gradient(self, canvas, width, height):
        """Create gradient on canvas"""
        # Simple horizontal gradient
        for i in range(width):
            # Calculate color interpolation
            ratio = i / width
            r1, g1, b1 = self._hex_to_rgb(self.color1)
            r2, g2, b2 = self._hex_to_rgb(self.color2)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(i, 0, i, height, fill=color, width=1)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class AnimatedButton(tk.Button):
    """Animated button with hover effects"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom properties
        self.normal_bg = kwargs.pop('normal_bg', '#4facfe')
        self.hover_bg = kwargs.pop('hover_bg', '#00f2fe')
        self.active_bg = kwargs.pop('active_bg', '#e74c3c')
        
        super().__init__(parent, bg=self.normal_bg, **kwargs)
        
        # Bind events for animation
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)
        
    def _on_enter(self, event):
        """Handle mouse enter"""
        self.config(bg=self.hover_bg)
        
    def _on_leave(self, event):
        """Handle mouse leave"""
        self.config(bg=self.normal_bg)
        
    def _on_click(self, event):
        """Handle mouse click"""
        self.config(bg=self.active_bg)
        
    def _on_release(self, event):
        """Handle mouse release"""
        self.config(bg=self.hover_bg)

class RoundedFrame(tk.Frame):
    """Frame with rounded corners effect"""
    
    def __init__(self, parent, corner_radius=10, **kwargs):
        super().__init__(parent, **kwargs)
        self.corner_radius = corner_radius
        self.bind('<Configure>', self._on_configure)
        
    def _on_configure(self, event=None):
        """Handle widget resize"""
        self._create_rounded_rectangle()
        
    def _create_rounded_rectangle(self):
        """Create rounded rectangle background"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Create canvas for rounded rectangle
        if hasattr(self, '_bg_canvas'):
            self._bg_canvas.destroy()
            
        self._bg_canvas = tk.Canvas(self, width=width, height=height, 
                                   highlightthickness=0)
        self._bg_canvas.place(x=0, y=0)
        
        # Draw rounded rectangle
        self._draw_rounded_rectangle(self._bg_canvas, 0, 0, width, height, 
                                   self.corner_radius, fill=self['bg'])
        
    def _draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Draw rounded rectangle on canvas"""
        points = []
        
        # Top side
        points.extend([x1 + radius, y1])
        points.extend([x2 - radius, y1])
        
        # Top right corner
        for i in range(90, 0, -1):
            angle = i * 3.14159 / 180
            x = x2 - radius + radius * tk.cos(angle)
            y = y1 + radius - radius * tk.sin(angle)
            points.extend([x, y])
            
        # Right side
        points.extend([x2, y1 + radius])
        points.extend([x2, y2 - radius])
        
        # Bottom right corner
        for i in range(0, -90, -1):
            angle = i * 3.14159 / 180
            x = x2 - radius + radius * tk.cos(angle)
            y = y2 - radius - radius * tk.sin(angle)
            points.extend([x, y])
            
        # Bottom side
        points.extend([x2 - radius, y2])
        points.extend([x1 + radius, y2])
        
        # Bottom left corner
        for i in range(-90, -180, -1):
            angle = i * 3.14159 / 180
            x = x1 + radius + radius * tk.cos(angle)
            y = y2 - radius - radius * tk.sin(angle)
            points.extend([x, y])
            
        # Left side
        points.extend([x1, y2 - radius])
        points.extend([x1, y1 + radius])
        
        # Top left corner
        for i in range(180, 90, -1):
            angle = i * 3.14159 / 180
            x = x1 + radius + radius * tk.cos(angle)
            y = y1 + radius - radius * tk.sin(angle)
            points.extend([x, y])
            
        canvas.create_polygon(points, smooth=True, **kwargs)
