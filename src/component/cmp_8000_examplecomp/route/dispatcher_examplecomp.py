# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-starter-py (See LICENCE)

"""Example component dispatcher."""

from core.dispatcher import Dispatcher


class DispatcherExampleComp(Dispatcher):
    """Example component dispatcher."""

    def __init__(self, request, comp_route, neutral_route=None):
        super().__init__(request, comp_route, neutral_route)
        self.schema_local_data['foo'] = "bar"

    def test1(self):
        """Business logic for test1 requests."""
        return True
        
    def get_features(self):
        """Return feature list for the example component."""
        features = [
            {"title": "Responsive Design", "desc": "Looks great on all devices"},
            {"title": "Bootstrap 5", "desc": "Modern UI framework"}, 
            {"title": "Easy Integration", "desc": "Simple to use components"},
            {"title": "Fast Loading", "desc": "Optimized performance"}
        ]
        return features
