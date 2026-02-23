"""ExampleComp Neutral plugin obj"""


def main(_params=None):
    """Main function."""
    
    # Sample data for the example component
    features = [
        {"title": "Responsive Design", "desc": "Looks great on all devices"},
        {"title": "Bootstrap 5", "desc": "Modern UI framework"}, 
        {"title": "Easy Integration", "desc": "Simple to use components"},
        {"title": "Fast Loading", "desc": "Optimized performance"}
    ]
    
    testimonials = [
        {"name": "John Doe", "role": "Developer", "comment": "Great component library!"},
        {"name": "Jane Smith", "role": "Designer", "comment": "Beautiful UI elements."}
    ]

    return {
        "data": {
            "message": "Welcome to the Example Component!",
            "subtitle": "A showcase of component capabilities",
            "features": features,
            "testimonials": testimonials
        }
    }
