import pandas as pd
import numpy as np

class EventImpactModel:
    def __init__(self):
        self.impact_matrix = None
        
    def build_impact_matrix(self, events, indicators):
        """Create event-indicator impact matrix"""
        # Initialize matrix
        self.impact_matrix = pd.DataFrame(
            0.0, 
            index=events, 
            columns=indicators
        )
        
        # Define impacts based on research
        # Telebirr launch impact
        if 'telebirr_launch' in events:
            self.impact_matrix.loc['telebirr_launch', 'ACC_MM_ACCOUNT'] = 0.05  # +5pp
            self.impact_matrix.loc['telebirr_launch', 'USG_DIGITAL_PAYMENT'] = 0.03
            
        # M-Pesa entry impact
        if 'mpesa_entry' in events:
            self.impact_matrix.loc['mpesa_entry', 'ACC_MM_ACCOUNT'] = 0.02
            self.impact_matrix.loc['mpesa_entry', 'ACC_OWNERSHIP'] = 0.01
            
        return self.impact_matrix
    
    def apply_impacts(self, baseline, events_list, year):
        """Apply event impacts to baseline projections"""
        adjusted = baseline.copy()
        
        for event in events_list:
            if event in self.impact_matrix.index:
                impacts = self.impact_matrix.loc[event]
                for indicator, impact in impacts.items():
                    if impact != 0 and indicator in adjusted.columns:
                        adjusted.loc[year, indicator] += impact
        
        return adjusted

if __name__ == "__main__":
    model = EventImpactModel()
    events = ['telebirr_launch', 'mpesa_entry', 'interoperability_launch']
    indicators = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']
    impact_matrix = model.build_impact_matrix(events, indicators)
    print("Event Impact Matrix:")
    print(impact_matrix)
