#!/usr/bin/env python3
"""
Argument Mapper for Discontinuity Thesis
Maps logical structure, dependencies, and assumptions
"""

import json
import os
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum

class ClaimType(Enum):
    EMPIRICAL = "empirical"  # Testable with data
    LOGICAL = "logical"      # Based on reasoning
    PHILOSOPHICAL = "philosophical"  # Value/belief based
    PREDICTION = "prediction"  # Future forecast

class EvidenceStrength(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NONE = "none"
    CONTRADICTORY = "contradictory"

@dataclass
class Assumption:
    """Represents an assumption in the thesis"""
    id: str
    description: str
    is_explicit: bool
    is_testable: bool
    criticality: str  # high/medium/low
    dependent_claims: List[str]

@dataclass
class Claim:
    """Represents a claim or argument in the thesis"""
    id: str
    statement: str
    claim_type: ClaimType
    source_essay: str
    assumptions: List[str]  # assumption ids
    depends_on: List[str]   # other claim ids
    evidence_for: Optional[str] = None
    evidence_against: Optional[str] = None
    strength_assessment: Optional[EvidenceStrength] = None
    notes: Optional[str] = None

class ArgumentMapper:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.claims: Dict[str, Claim] = {}
        self.assumptions: Dict[str, Assumption] = {}
        self.load_existing_analysis()
    
    def load_existing_analysis(self):
        """Load any existing analysis from JSON files"""
        analysis_file = "analysis/argument-map.json"
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r') as f:
                data = json.load(f)
                # Reconstruct claims and assumptions from JSON
                for claim_data in data.get('claims', []):
                    claim = Claim(**claim_data)
                    claim.claim_type = ClaimType(claim_data['claim_type'])
                    if claim_data.get('strength_assessment'):
                        claim.strength_assessment = EvidenceStrength(claim_data['strength_assessment'])
                    self.claims[claim.id] = claim
                
                for assumption_data in data.get('assumptions', []):
                    assumption = Assumption(**assumption_data)
                    self.assumptions[assumption.id] = assumption
    
    def add_claim(self, claim: Claim):
        """Add a claim to the map"""
        self.claims[claim.id] = claim
    
    def add_assumption(self, assumption: Assumption):
        """Add an assumption to the map"""
        self.assumptions[assumption.id] = assumption
    
    def get_dependency_chain(self, claim_id: str, visited: Optional[Set[str]] = None) -> List[str]:
        """Get all claims that a given claim depends on"""
        if visited is None:
            visited = set()
        
        if claim_id in visited or claim_id not in self.claims:
            return []
        
        visited.add(claim_id)
        chain = [claim_id]
        
        claim = self.claims[claim_id]
        for dep_id in claim.depends_on:
            chain.extend(self.get_dependency_chain(dep_id, visited))
        
        return chain
    
    def get_critical_assumptions(self) -> List[Assumption]:
        """Get all assumptions marked as critical"""
        return [a for a in self.assumptions.values() if a.criticality == "high"]
    
    def get_testable_claims(self) -> List[Claim]:
        """Get all empirical/testable claims"""
        return [c for c in self.claims.values() if c.claim_type == ClaimType.EMPIRICAL]
    
    def analyze_assumption_impact(self, assumption_id: str) -> Dict:
        """Analyze what fails if an assumption is false"""
        if assumption_id not in self.assumptions:
            return {}
        
        assumption = self.assumptions[assumption_id]
        affected_claims = []
        
        for claim_id in assumption.dependent_claims:
            if claim_id in self.claims:
                affected_claims.append({
                    'claim_id': claim_id,
                    'statement': self.claims[claim_id].statement,
                    'dependency_chain': self.get_dependency_chain(claim_id)
                })
        
        return {
            'assumption': assumption.description,
            'criticality': assumption.criticality,
            'affected_claims': affected_claims,
            'total_impact': len(affected_claims)
        }
    
    def generate_evaluation_matrix(self) -> List[Dict]:
        """Generate claim evaluation matrix"""
        matrix = []
        for claim in self.claims.values():
            matrix.append({
                'id': claim.id,
                'statement': claim.statement,
                'type': claim.claim_type.value,
                'evidence_for': claim.evidence_for or "Not evaluated",
                'evidence_against': claim.evidence_against or "Not evaluated",
                'strength': claim.strength_assessment.value if claim.strength_assessment else "Not assessed",
                'testable': claim.claim_type == ClaimType.EMPIRICAL,
                'notes': claim.notes or ""
            })
        return matrix
    
    def save_analysis(self):
        """Save current analysis to JSON"""
        os.makedirs("analysis", exist_ok=True)
        
        # Convert to serializable format
        claims_data = []
        for claim in self.claims.values():
            claim_dict = asdict(claim)
            claim_dict['claim_type'] = claim.claim_type.value
            if claim.strength_assessment:
                claim_dict['strength_assessment'] = claim.strength_assessment.value
            claims_data.append(claim_dict)
        
        assumptions_data = [asdict(a) for a in self.assumptions.values()]
        
        output = {
            'claims': claims_data,
            'assumptions': assumptions_data,
            'statistics': {
                'total_claims': len(self.claims),
                'total_assumptions': len(self.assumptions),
                'testable_claims': len(self.get_testable_claims()),
                'critical_assumptions': len(self.get_critical_assumptions())
            }
        }
        
        with open("analysis/argument-map.json", 'w') as f:
            json.dump(output, f, indent=2)
        
        # Also save evaluation matrix
        matrix = self.generate_evaluation_matrix()
        with open("analysis/evaluation-matrix.json", 'w') as f:
            json.dump(matrix, f, indent=2)
        
        print(f"Analysis saved: {len(self.claims)} claims, {len(self.assumptions)} assumptions")
    
    def generate_report(self) -> str:
        """Generate a markdown report of the analysis"""
        report = ["# Argument Structure Analysis\n"]
        
        # Statistics
        report.append("## Overview Statistics")
        report.append(f"- Total Claims: {len(self.claims)}")
        report.append(f"- Total Assumptions: {len(self.assumptions)}")
        report.append(f"- Testable Claims: {len(self.get_testable_claims())}")
        report.append(f"- Critical Assumptions: {len(self.get_critical_assumptions())}\n")
        
        # Critical Assumptions
        report.append("## Critical Assumptions")
        for assumption in self.get_critical_assumptions():
            impact = self.analyze_assumption_impact(assumption.id)
            report.append(f"\n### {assumption.description}")
            report.append(f"- **Testable**: {assumption.is_testable}")
            report.append(f"- **Explicit**: {assumption.is_explicit}")
            report.append(f"- **Impact**: Affects {impact['total_impact']} claims")
        
        # Testable Claims
        report.append("\n## Testable Claims")
        for claim in self.get_testable_claims():
            report.append(f"\n### {claim.statement}")
            report.append(f"- **Source**: {claim.source_essay}")
            report.append(f"- **Evidence For**: {claim.evidence_for or 'Not evaluated'}")
            report.append(f"- **Evidence Against**: {claim.evidence_against or 'Not evaluated'}")
            if claim.strength_assessment:
                report.append(f"- **Strength**: {claim.strength_assessment.value}")
        
        return "\n".join(report)


# Initialize core thesis claims and assumptions
def initialize_thesis_structure():
    """Initialize the thesis with core claims and assumptions from our analysis"""
    mapper = ArgumentMapper()
    
    # Core Assumptions
    assumptions = [
        Assumption(
            id="A1",
            description="AI capabilities will continue improving exponentially",
            is_explicit=False,
            is_testable=True,
            criticality="high",
            dependent_claims=["C1", "C2", "C3"]
        ),
        Assumption(
            id="A2",
            description="Verification requires rare, unteachable skills",
            is_explicit=True,
            is_testable=True,
            criticality="high",
            dependent_claims=["C4", "C5"]
        ),
        Assumption(
            id="A3",
            description="No new job categories will emerge fast enough",
            is_explicit=True,
            is_testable=True,
            criticality="high",
            dependent_claims=["C1", "C6"]
        ),
        Assumption(
            id="A4",
            description="AI + verifier is 100x cheaper than human labor",
            is_explicit=True,
            is_testable=True,
            criticality="high",
            dependent_claims=["C2", "C7"]
        ),
        Assumption(
            id="A5",
            description="Physical jobs cannot absorb cognitive workers",
            is_explicit=True,
            is_testable=True,
            criticality="medium",
            dependent_claims=["C6", "C8"]
        )
    ]
    
    # Core Claims
    claims = [
        Claim(
            id="C1",
            statement="AI represents a discontinuity from all previous technological revolutions",
            claim_type=ClaimType.PHILOSOPHICAL,
            source_essay="the-original-discontinuity-thesis",
            assumptions=["A1", "A3"],
            depends_on=[]
        ),
        Claim(
            id="C2",
            statement="Mass unemployment is mechanically inevitable",
            claim_type=ClaimType.PREDICTION,
            source_essay="the-engine-of-obsolescence",
            assumptions=["A1", "A4"],
            depends_on=["C1"]
        ),
        Claim(
            id="C3",
            statement="AI automates cognition itself, not just tasks",
            claim_type=ClaimType.LOGICAL,
            source_essay="the-original-discontinuity-thesis",
            assumptions=["A1"],
            depends_on=[]
        ),
        Claim(
            id="C4",
            statement="Only 5% of workers can effectively verify AI output",
            claim_type=ClaimType.EMPIRICAL,
            source_essay="the-ai-verification-divide",
            assumptions=["A2"],
            depends_on=[]
        ),
        Claim(
            id="C5",
            statement="The verification divide creates permanent stratification",
            claim_type=ClaimType.PREDICTION,
            source_essay="the-ai-verification-divide",
            assumptions=["A2"],
            depends_on=["C4"]
        ),
        Claim(
            id="C6",
            statement="There is no exit strategy for displaced workers",
            claim_type=ClaimType.LOGICAL,
            source_essay="the-original-discontinuity-thesis",
            assumptions=["A3", "A5"],
            depends_on=["C1", "C3"]
        ),
        Claim(
            id="C7",
            statement="The Engine of Obsolescence operates mechanically",
            claim_type=ClaimType.LOGICAL,
            source_essay="the-engine-of-obsolescence",
            assumptions=["A4"],
            depends_on=[]
        ),
        Claim(
            id="C8",
            statement="Physical refuge is mathematically insufficient",
            claim_type=ClaimType.EMPIRICAL,
            source_essay="the-original-discontinuity-thesis",
            assumptions=["A5"],
            depends_on=[]
        )
    ]
    
    # Add to mapper
    for assumption in assumptions:
        mapper.add_assumption(assumption)
    
    for claim in claims:
        mapper.add_claim(claim)
    
    return mapper


if __name__ == "__main__":
    # Initialize and save the thesis structure
    mapper = initialize_thesis_structure()
    mapper.save_analysis()
    
    # Generate and save report
    report = mapper.generate_report()
    with open("analysis/argument-structure-report.md", 'w') as f:
        f.write(report)
    
    print("Argument structure analysis complete")
    print(f"Report saved to analysis/argument-structure-report.md")