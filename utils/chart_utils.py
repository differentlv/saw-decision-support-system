import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict
from assets.styles import AppStyles


class ChartGenerator:
    """Generate charts for SAW results"""
    
    def create_saw_charts(self, results: List[Tuple[str, float]]):
        """Create bar and pie charts for SAW results"""
        if not results:
            raise ValueError("No results to visualize")
        
        # Prepare data
        alternatives = [result[0] for result in results]
        scores = [result[1] for result in results]
        colors = AppStyles.get_color_palette(len(alternatives))
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bar chart
        bars = ax1.bar(alternatives, scores, color=colors)
        ax1.set_title('Skor SAW per Alternatif', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Alternatif')
        ax1.set_ylabel('Skor SAW')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{score:.3f}', ha='center', va='bottom')
        
        # Pie chart
        ax2.pie(scores, labels=alternatives, autopct='%1.2f%%', 
               startangle=90, colors=colors)
        ax2.set_title('Proporsi Skor SAW', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig


class SensitivityChartGenerator:
    """Generate charts for sensitivity analysis"""
    
    def create_sensitivity_chart(self, sensitivity_results: List[Dict], criteria_name: str):
        """Create sensitivity analysis chart"""
        if not sensitivity_results:
            raise ValueError("No sensitivity results to visualize")
        
        # Prepare data
        changes = [result['change'] for result in sensitivity_results]
        scores = [result['score'] for result in sensitivity_results]
        winners = [result['winner'] for result in sensitivity_results]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color map for different winners
        unique_winners = list(set(winners))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_winners)))
        color_map = {winner: colors[i] for i, winner in enumerate(unique_winners)}
        
        point_colors = [color_map[winner] for winner in winners]
        
        # Scatter plot
        scatter = ax.scatter(changes, scores, c=point_colors, s=50, alpha=0.7)
        ax.plot(changes, scores, 'k-', alpha=0.3)
        
        ax.set_xlabel(f'Perubahan Bobot {criteria_name}')
        ax.set_ylabel('Skor SAW Terbaik')
        ax.set_title(f'Analisis Sensitivitas - {criteria_name}', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                    markerfacecolor=color_map[winner], 
                                    markersize=8, label=winner)
                         for winner in unique_winners]
        ax.legend(handles=legend_elements, loc='best')
        
        plt.tight_layout()
        return fig
    
    def create_stability_chart(self, sensitivity_results: List[Dict], 
                             original_winner: str, criteria_name: str):
        """Create stability visualization chart"""
        if not sensitivity_results:
            raise ValueError("No sensitivity results to visualize")
        
        # Prepare data
        changes = [result['change'] for result in sensitivity_results]
        winners = [result['winner'] for result in sensitivity_results]
        
        # Calculate stability at each point
        stability_points = []
        for i, winner in enumerate(winners):
            if winner == original_winner:
                stability_points.append(1)
            else:
                stability_points.append(0)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Bar chart showing stability
        colors = ['green' if stable else 'red' for stable in stability_points]
        bars = ax.bar(changes, stability_points, color=colors, alpha=0.6)
        
        ax.set_xlabel(f'Perubahan Bobot {criteria_name}')
        ax.set_ylabel('Stabilitas (1 = Stabil, 0 = Berubah)')
        ax.set_title(f'Stabilitas Keputusan - {criteria_name}', 
                    fontsize=14, fontweight='bold')
        ax.set_ylim(-0.1, 1.1)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add stability percentage as text
        stability_pct = sum(stability_points) / len(stability_points) * 100
        ax.text(0.02, 0.98, f'Stabilitas: {stability_pct:.1f}%', 
               transform=ax.transAxes, fontsize=12, fontweight='bold',
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        return fig


class ComparisonChartGenerator:
    """Generate comparison charts for multiple scenarios"""
    
    def create_comparison_chart(self, scenarios: Dict[str, List[Tuple[str, float]]]):
        """Create comparison chart for multiple scenarios"""
        if not scenarios:
            raise ValueError("No scenarios to compare")
        
        # Prepare data
        scenario_names = list(scenarios.keys())
        all_alternatives = set()
        for results in scenarios.values():
            all_alternatives.update([alt for alt, _ in results])
        all_alternatives = sorted(list(all_alternatives))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Bar width
        bar_width = 0.8 / len(scenario_names)
        x_pos = np.arange(len(all_alternatives))
        
        # Plot bars for each scenario
        for i, (scenario_name, results) in enumerate(scenarios.items()):
            scores = []
            for alt in all_alternatives:
                score = next((score for name, score in results if name == alt), 0)
                scores.append(score)
            
            bars = ax.bar(x_pos + i * bar_width, scores, bar_width, 
                         label=scenario_name, alpha=0.8)
        
        ax.set_xlabel('Alternatif')
        ax.set_ylabel('Skor SAW')
        ax.set_title('Perbandingan Skor SAW Antar Skenario', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos + bar_width * (len(scenario_names) - 1) / 2)
        ax.set_xticklabels(all_alternatives, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig