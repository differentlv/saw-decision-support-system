import numpy as np
from typing import List, Tuple, Dict, Any


class SAWModel:
    """SAW calculation model"""
    
    def __init__(self):
        self.alternatives = []
        self.criteria = []
        self.weights = []
        self.decision_matrix = []
        self.criteria_types = []  # 'benefit' or 'cost'
        self.results = []
        self.normalized_matrix = None
        
    def set_data(self, alternatives: List[str], criteria: List[str], 
        weights: List[float], decision_matrix: List[List[float]], 
        criteria_types: List[str]):
        """Set all data for SAW calculation"""
        self.alternatives = alternatives.copy()
        self.criteria = criteria.copy()
        self.weights = weights.copy()
        self.decision_matrix = [row.copy() for row in decision_matrix]
        self.criteria_types = criteria_types.copy()
        
        # Normalize weights
        total_weight = sum(self.weights)
        if total_weight > 0:
            self.weights = [w/total_weight for w in self.weights]
    
    def normalize_matrix(self) -> np.ndarray:
        """Normalize the decision matrix"""
        if not self.decision_matrix:
            raise ValueError("Decision matrix is empty")
            
        matrix = np.array(self.decision_matrix)
        normalized_matrix = np.zeros_like(matrix, dtype=float)
        
        for j in range(len(self.criteria)):
            if self.criteria_types[j] == 'benefit':
                # For benefit criteria: R_ij = X_ij / max(X_ij)
                max_val = np.max(matrix[:, j])
                if max_val > 0:
                    normalized_matrix[:, j] = matrix[:, j] / max_val
            else:
                # For cost criteria: R_ij = min(X_ij) / X_ij
                min_val = np.min(matrix[:, j])
                if min_val > 0:
                    normalized_matrix[:, j] = min_val / matrix[:, j]
        
        self.normalized_matrix = normalized_matrix
        return normalized_matrix
    
    def calculate_scores(self) -> List[Tuple[str, float]]:
        """Calculate SAW scores for all alternatives"""
        if self.normalized_matrix is None:
            self.normalize_matrix()
        
        scores = []
        for i, alt in enumerate(self.alternatives):
            score = np.sum(np.array(self.weights) * self.normalized_matrix[i, :])
            scores.append((alt, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        self.results = scores
        return scores
    
    def get_calculation_steps(self) -> Dict[str, Any]:
        """Get detailed calculation steps for display"""
        if not self.decision_matrix:
            raise ValueError("No data available for calculation")
        
        matrix = np.array(self.decision_matrix)
        normalized_matrix = self.normalize_matrix()
        scores = self.calculate_scores()
        
        steps = {
            'original_matrix': matrix,
            'normalized_matrix': normalized_matrix,
            'weights': self.weights,
            'scores': scores,
            'alternatives': self.alternatives,
            'criteria': self.criteria,
            'criteria_types': self.criteria_types
        }
        
        return steps
    
    def sensitivity_analysis(self, criteria_index: int, weight_range: float) -> List[Dict]:
        """Perform sensitivity analysis on a specific criteria"""
        if not self.results:
            raise ValueError("No results available. Calculate SAW first.")
        
        original_weight = self.weights[criteria_index]
        weight_changes = np.arange(-weight_range, weight_range + 0.01, 0.02)
        sensitivity_results = []
        
        matrix = np.array(self.decision_matrix)
        
        for change in weight_changes:
            new_weight = original_weight + change
            if new_weight <= 0 or new_weight >= 1:
                continue
            
            # Adjust weights
            temp_weights = self.weights.copy()
            temp_weights[criteria_index] = new_weight
            
            # Renormalize other weights
            other_weights_sum = sum(temp_weights) - new_weight
            if other_weights_sum > 0:
                for i in range(len(temp_weights)):
                    if i != criteria_index:
                        temp_weights[i] = temp_weights[i] * (1 - new_weight) / other_weights_sum
            
            # Recalculate scores with new weights
            scores = []
            for i in range(len(self.alternatives)):
                score = np.sum(temp_weights * self.normalized_matrix[i, :])
                scores.append((self.alternatives[i], score))
            
            scores.sort(key=lambda x: x[1], reverse=True)
            
            sensitivity_results.append({
                'change': change,
                'new_weight': new_weight,
                'winner': scores[0][0],
                'score': scores[0][1],
                'full_results': scores
            })
        
        return sensitivity_results
    
    def calculate_stability(self, sensitivity_results: List[Dict]) -> Dict[str, Any]:
        """Calculate decision stability from sensitivity analysis"""
        if not sensitivity_results or not self.results:
            return {'stability': 0, 'level': 'TIDAK STABIL'}
        
        original_winner = self.results[0][0]
        winners = [result['winner'] for result in sensitivity_results]
        stability = winners.count(original_winner) / len(winners) * 100 if winners else 0
        
        if stability >= 80:
            level = 'SANGAT STABIL'
        elif stability >= 60:
            level = 'STABIL'
        elif stability >= 40:
            level = 'CUKUP STABIL'
        else:
            level = 'TIDAK STABIL'
        
        return {
            'stability': stability,
            'level': level,
            'original_winner': original_winner,
            'winners': winners
        }
    
    def reset(self):
        """Reset all data"""
        self.alternatives = []
        self.criteria = []
        self.weights = []
        self.decision_matrix = []
        self.criteria_types = []
        self.results = []
        self.normalized_matrix = None