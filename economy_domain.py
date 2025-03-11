"""
Economy Domain Module

This module implements the Economy domain from the Life Dimensions framework,
representing our relationship with material resources, financial systems, and value exchange.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
import math
import random


class ResourceType(Enum):
    """Types of resources in the Economy domain"""
    MONEY = "money"
    TIME = "time"
    ENERGY = "energy"
    ASSETS = "assets"
    SKILLS = "skills"


class DevelopmentalStage(Enum):
    """Developmental stages of the Economy domain"""
    DEPENDENT = 1
    SURVIVAL = 2
    STABILITY = 3
    GROWTH = 4
    ABUNDANCE = 5


@dataclass
class Resource:
    """Represents a resource in the Economy domain"""
    type: ResourceType
    quantity: float
    quality: float  # 0.0 to 1.0
    renewable: bool = False
    
    @property
    def value(self) -> float:
        """Calculate the overall value of the resource"""
        return self.quantity * self.quality * (1.5 if self.renewable else 1.0)


class FinancialDecision:
    """Represents a financial decision with game theory principles"""
    
    def __init__(self, name: str, risk: float, potential_return: float, 
                 time_horizon: int, alignment_with_values: float):
        """
        Initialize a financial decision
        
        Args:
            name: Name of the decision
            risk: Risk level (0.0 to 1.0)
            potential_return: Potential return multiplier
            time_horizon: Time needed for returns (in arbitrary units)
            alignment_with_values: How aligned with personal values (0.0 to 1.0)
        """
        self.name = name
        self.risk = max(0.0, min(1.0, risk))
        self.potential_return = potential_return
        self.time_horizon = time_horizon
        self.alignment_with_values = max(0.0, min(1.0, alignment_with_values))
    
    def expected_value(self, risk_tolerance: float) -> float:
        """
        Calculate expected value based on risk tolerance
        
        Args:
            risk_tolerance: Individual's risk tolerance (0.0 to 1.0)
            
        Returns:
            Expected value of the decision
        """
        risk_factor = 1.0 - abs(self.risk - risk_tolerance)
        value_factor = 1.0 + self.alignment_with_values
        time_discount = 1.0 / (1.0 + 0.1 * self.time_horizon)
        
        return self.potential_return * risk_factor * value_factor * time_discount
    
    def make_decision(self, risk_tolerance: float, random_factor: float = 0.1) -> bool:
        """
        Determine if this decision should be made
        
        Args:
            risk_tolerance: Individual's risk tolerance (0.0 to 1.0)
            random_factor: Randomness in decision making (0.0 to 1.0)
            
        Returns:
            True if the decision should be made, False otherwise
        """
        expected_value = self.expected_value(risk_tolerance)
        threshold = 1.0 + (random.random() - 0.5) * random_factor
        return expected_value > threshold


class EconomyDomain:
    """
    Represents the Economy domain from the Life Dimensions framework
    """
    
    def __init__(self, initial_resources: Optional[List[Resource]] = None):
        """Initialize the Economy domain with resources"""
        self.resources = initial_resources or []
        self.developmental_stage = DevelopmentalStage.DEPENDENT
        self.financial_literacy = 0.0  # 0.0 to 1.0
        self.risk_tolerance = 0.5  # 0.0 to 1.0
        self.generosity_index = 0.0  # 0.0 to 1.0
        self.decisions_history: List[FinancialDecision] = []
        self.balance_score = 0.5  # 0.0 to 1.0
        
    @property
    def total_wealth(self) -> float:
        """Calculate total wealth across all resources"""
        return sum(resource.value for resource in self.resources)
    
    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the economy domain"""
        self.resources.append(resource)
        self._recalculate_developmental_stage()
    
    def consume_resource(self, resource_type: ResourceType, amount: float) -> bool:
        """
        Consume a specified amount of a resource
        
        Returns:
            True if successful, False if insufficient resources
        """
        for i, resource in enumerate(self.resources):
            if resource.type == resource_type:
                if resource.quantity >= amount:
                    self.resources[i].quantity -= amount
                    if self.resources[i].quantity <= 0:
                        self.resources.pop(i)
                    return True
        return False
    
    def make_investment(self, decision: FinancialDecision) -> bool:
        """
        Make an investment based on a financial decision
        
        Returns:
            True if the investment was made, False otherwise
        """
        should_invest = decision.make_decision(self.risk_tolerance)
        if should_invest:
            self.decisions_history.append(decision)
        return should_invest
    
    def give_resources(self, resource_type: ResourceType, amount: float) -> bool:
        """
        Give resources to others (implements the Giving spiritual law)
        
        Returns:
            True if successful, False if insufficient resources
        """
        success = self.consume_resource(resource_type, amount)
        if success:
            self.generosity_index = min(1.0, self.generosity_index + 0.05)
            # The act of giving increases abundance according to the spiritual law
            self._apply_giving_law()
        return success
    
    def _apply_giving_law(self) -> None:
        """Apply the spiritual law of Giving to create abundance"""
        # Simplified implementation of the giving law
        # In a real system, this would be more complex
        if random.random() < self.generosity_index:
            new_resource = Resource(
                type=random.choice(list(ResourceType)),
                quantity=random.uniform(1.0, 5.0) * self.generosity_index,
                quality=min(1.0, 0.5 + self.generosity_index / 2),
                renewable=random.random() > 0.5
            )
            self.add_resource(new_resource)
    
    def _recalculate_developmental_stage(self) -> None:
        """Recalculate the developmental stage based on current resources"""
        total_wealth = self.total_wealth
        
        if total_wealth < 10:
            self.developmental_stage = DevelopmentalStage.DEPENDENT
        elif total_wealth < 50:
            self.developmental_stage = DevelopmentalStage.SURVIVAL
        elif total_wealth < 100:
            self.developmental_stage = DevelopmentalStage.STABILITY
        elif total_wealth < 200:
            self.developmental_stage = DevelopmentalStage.GROWTH
        else:
            self.developmental_stage = DevelopmentalStage.ABUNDANCE
    
    def financial_model(self, time_periods: int, 
                        external_factors: Dict[str, float] = None) -> List[float]:
        """
        Create a financial model projecting wealth over time
        
        Args:
            time_periods: Number of time periods to model
            external_factors: Dictionary of external factors affecting the model
            
        Returns:
            List of projected wealth values for each time period
        """
        factors = external_factors or {}
        inflation = factors.get('inflation', 0.03)
        growth_rate = factors.get('growth_rate', 0.07)
        volatility = factors.get('volatility', 0.15)
        
        # Apply game theory and conservation of energy principles
        effective_growth = growth_rate * (1 + self.financial_literacy / 2)
        risk_adjusted_growth = effective_growth * (1 - self.risk_tolerance * volatility / 2)
        
        wealth_projection = [self.total_wealth]
        current_wealth = self.total_wealth
        
        for _ in range(time_periods):
            # Conservation of energy principle - value transforms but doesn't disappear
            random_factor = 1.0 + random.normalvariate(0, volatility)
            growth_factor = 1.0 + (risk_adjusted_growth - inflation) * random_factor
            
            # Apply giving law effect
            giving_factor = 1.0 + (self.generosity_index * 0.05)
            
            current_wealth *= growth_factor * giving_factor
            wealth_projection.append(current_wealth)
            
        return wealth_projection
    
    def balance_check(self) -> Dict[str, float]:
        """
        Check the balance of the Economy domain
        
        Returns:
            Dictionary with balance metrics
        """
        # Calculate metrics based on the shadow aspect (Greed) and spiritual law (Giving)
        greed_factor = 1.0 - self.generosity_index
        material_attachment = sum(1 for d in self.decisions_history 
                                if d.alignment_with_values < 0.5) / max(1, len(self.decisions_history))
        
        resource_diversity = len(set(r.type for r in self.resources)) / len(ResourceType)
        
        balance = {
            'greed_factor': greed_factor,
            'material_attachment': material_attachment,
            'resource_diversity': resource_diversity,
            'overall_balance': 1.0 - (greed_factor + material_attachment) / 2 + resource_diversity / 2
        }
        
        self.balance_score = balance['overall_balance']
        return balance


# Example usage
if __name__ == "__main__":
    # Create an Economy domain instance
    economy = EconomyDomain([
        Resource(ResourceType.MONEY, 1000.0, 1.0),
        Resource(ResourceType.TIME, 40.0, 0.8, renewable=True),
        Resource(ResourceType.SKILLS, 5.0, 0.7, renewable=True)
    ])
    
    # Make some financial decisions
    investment = FinancialDecision(
        name="Stock Market Investment",
        risk=0.6,
        potential_return=1.8,
        time_horizon=5,
        alignment_with_values=0.7
    )
    
    if economy.make_investment(investment):
        print(f"Decided to invest in {investment.name}")
    
    # Practice giving
    if economy.give_resources(ResourceType.MONEY, 100.0):
        print("Gave away some money, practicing the spiritual law of Giving")
    
    # Check developmental stage
    print(f"Current developmental stage: {economy.developmental_stage.name}")
    
    # Create a financial model
    projection = economy.financial_model(10, {'inflation': 0.04, 'volatility': 0.2})
    print(f"Wealth projection over 10 time periods: {[round(w, 2) for w in projection]}")
    
    # Check balance
    balance = economy.balance_check()
    print(f"Economy domain balance: {balance['overall_balance']:.2f}")
