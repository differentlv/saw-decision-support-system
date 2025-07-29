class AppConfig:
    """Application configuration constants"""
    
    # Window settings
    WINDOW_TITLE = "Sistem Pendukung Keputusan - Metode SAW"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WIDTH = 1000
    MIN_HEIGHT = 600
    
    # Theme settings
    THEME = 'clam'
    BACKGROUND_COLOR = '#f0f0f0'
    
    # Font settings
    TITLE_FONT = ('Arial', 16, 'bold')
    HEADING_FONT = ('Arial', 12, 'bold')
    NORMAL_FONT = ('Arial', 10)
    MONOSPACE_FONT = ('Courier', 10)
    
    # Color scheme
    PRIMARY_COLOR = '#2E8B57'
    PRIMARY_ACTIVE = '#228B22'
    SUCCESS_COLOR = '#2C8F47'
    DANGER_COLOR = '#f33b3b'
    
    # Export settings
    EXPORT_DATE_FORMAT = "%Y%m%d_%H%M%S"
    EXPORT_FILENAME_PREFIX = "hasil_saw_"
    
    # Calculation settings
    DEFAULT_SENSITIVITY_RANGE = 0.2
    SENSITIVITY_STEP = 0.02
    STABILITY_THRESHOLDS = {
        'very_stable': 80,
        'stable': 60,
        'moderate': 40
    }
    
    # Group members
    GROUP_MEMBERS = [
        "RAIHAN ALVIAN NURYANSYAH"
    ]