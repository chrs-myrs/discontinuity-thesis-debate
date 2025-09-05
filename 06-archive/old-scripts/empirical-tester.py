#!/usr/bin/env python3
"""
Empirical Testing Framework for Discontinuity Thesis
Tests specific claims against collected data
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class TestResult(Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    INCONCLUSIVE = "inconclusive"
    INSUFFICIENT_DATA = "insufficient_data"

class DataQuality(Enum):
    HIGH = "high"      # Peer-reviewed, recent, large sample
    MEDIUM = "medium"  # Credible source, reasonable methodology
    LOW = "low"        # Blog posts, opinions, small samples

@dataclass
class DataPoint:
    """Represents a piece of evidence"""
    id: str
    source: str
    date: str
    quality: DataQuality
    summary: str
    url: Optional[str] = None
    raw_data: Optional[Dict] = None

@dataclass
class EmpiricalTest:
    """Represents a test of a specific claim"""
    test_id: str
    claim_id: str
    claim_text: str
    hypothesis: str
    null_hypothesis: str
    data_needed: List[str]
    success_criteria: str
    data_points: List[DataPoint]
    result: Optional[TestResult] = None
    confidence: Optional[float] = None  # 0-1 scale
    analysis: Optional[str] = None

class EmpiricalTester:
    def __init__(self):
        self.tests: Dict[str, EmpiricalTest] = {}
        self.data_points: Dict[str, DataPoint] = {}
        self.load_existing_tests()
        self.initialize_tests()
    
    def load_existing_tests(self):
        """Load any existing test results"""
        test_file = "analysis/empirical-tests.json"
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                data = json.load(f)
                for test_data in data.get('tests', []):
                    test = self._dict_to_test(test_data)
                    self.tests[test.test_id] = test
    
    def _dict_to_test(self, data: Dict) -> EmpiricalTest:
        """Convert dictionary to EmpiricalTest object"""
        test = EmpiricalTest(**{k: v for k, v in data.items() if k != 'data_points'})
        test.data_points = [DataPoint(**dp) for dp in data.get('data_points', [])]
        if data.get('result'):
            test.result = TestResult(data['result'])
        return test
    
    def initialize_tests(self):
        """Set up core empirical tests for the thesis"""
        
        # Test 1: The 5% Verification Claim
        if "T1" not in self.tests:
            self.tests["T1"] = EmpiricalTest(
                test_id="T1",
                claim_id="C4",
                claim_text="Only 5% of workers can effectively verify AI output",
                hypothesis="Less than or equal to 5% of workers can effectively verify AI output",
                null_hypothesis="More than 5% of workers can effectively verify AI output",
                data_needed=[
                    "Studies on AI tool usage effectiveness",
                    "Surveys of AI verification capabilities",
                    "Training program success rates"
                ],
                success_criteria="Find studies showing actual percentage of effective AI users",
                data_points=[]
            )
        
        # Test 2: The 100x Cost Advantage
        if "T2" not in self.tests:
            self.tests["T2"] = EmpiricalTest(
                test_id="T2",
                claim_id="A4",
                claim_text="AI + verifier is 100x cheaper than human labor",
                hypothesis="AI + verification costs < 1% of human labor costs",
                null_hypothesis="AI + verification costs >= 1% of human labor costs",
                data_needed=[
                    "AI operational costs",
                    "Human verification time/costs",
                    "Error correction costs",
                    "Total cost comparisons"
                ],
                success_criteria="Calculate actual cost ratios with hidden costs included",
                data_points=[]
            )
        
        # Test 3: No New Job Categories
        if "T3" not in self.tests:
            self.tests["T3"] = EmpiricalTest(
                test_id="T3",
                claim_id="A3",
                claim_text="No new job categories will emerge fast enough",
                hypothesis="New AI-related jobs < displaced jobs in same period",
                null_hypothesis="New AI-related jobs >= displaced jobs",
                data_needed=[
                    "New job category creation rates",
                    "AI displacement statistics",
                    "Timeline comparisons"
                ],
                success_criteria="Compare job creation vs destruction rates 2020-2024",
                data_points=[]
            )
        
        # Test 4: Physical Jobs Can't Absorb
        if "T4" not in self.tests:
            self.tests["T4"] = EmpiricalTest(
                test_id="T4",
                claim_id="C8",
                claim_text="Physical refuge is mathematically insufficient",
                hypothesis="Physical job capacity < displaced cognitive workers",
                null_hypothesis="Physical jobs can absorb significant displaced workers",
                data_needed=[
                    "Physical job growth rates",
                    "Cognitive worker displacement numbers",
                    "Retraining success rates"
                ],
                success_criteria="Calculate absorption capacity vs displacement volume",
                data_points=[]
            )
        
        # Test 5: Exponential AI Improvement
        if "T5" not in self.tests:
            self.tests["T5"] = EmpiricalTest(
                test_id="T5",
                claim_id="A1",
                claim_text="AI capabilities will continue improving exponentially",
                hypothesis="AI performance metrics show exponential growth",
                null_hypothesis="AI performance shows linear or plateauing growth",
                data_needed=[
                    "AI benchmark performance over time",
                    "Cost-performance curves",
                    "Capability frontier evolution"
                ],
                success_criteria="Identify trend in AI capability metrics 2020-2024",
                data_points=[]
            )
    
    def add_data_point(self, test_id: str, data_point: DataPoint):
        """Add evidence to a specific test"""
        if test_id in self.tests:
            self.tests[test_id].data_points.append(data_point)
            self.data_points[data_point.id] = data_point
    
    def evaluate_test(self, test_id: str) -> Tuple[TestResult, float]:
        """Evaluate a test based on collected data"""
        if test_id not in self.tests:
            return TestResult.INSUFFICIENT_DATA, 0.0
        
        test = self.tests[test_id]
        
        if not test.data_points:
            return TestResult.INSUFFICIENT_DATA, 0.0
        
        # Weight data points by quality
        quality_weights = {
            DataQuality.HIGH: 1.0,
            DataQuality.MEDIUM: 0.6,
            DataQuality.LOW: 0.3
        }
        
        supports = 0
        contradicts = 0
        total_weight = 0
        
        # This is simplified - real evaluation would parse the actual data
        for dp in test.data_points:
            weight = quality_weights[dp.quality]
            total_weight += weight
            
            # In practice, we'd analyze dp.raw_data to determine support
            # For now, this is a placeholder
            if "support" in dp.summary.lower():
                supports += weight
            elif "contradict" in dp.summary.lower():
                contradicts += weight
        
        if total_weight == 0:
            return TestResult.INSUFFICIENT_DATA, 0.0
        
        support_ratio = supports / total_weight
        contradict_ratio = contradicts / total_weight
        
        if support_ratio > 0.6:
            result = TestResult.SUPPORTS
            confidence = support_ratio
        elif contradict_ratio > 0.6:
            result = TestResult.CONTRADICTS
            confidence = contradict_ratio
        else:
            result = TestResult.INCONCLUSIVE
            confidence = 1.0 - abs(support_ratio - contradict_ratio)
        
        test.result = result
        test.confidence = confidence
        
        return result, confidence
    
    def generate_test_report(self) -> str:
        """Generate a report of all empirical tests"""
        report = ["# Empirical Test Results\n"]
        report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        # Summary statistics
        total_tests = len(self.tests)
        evaluated = sum(1 for t in self.tests.values() if t.result)
        
        report.append("## Summary")
        report.append(f"- Total Tests: {total_tests}")
        report.append(f"- Evaluated: {evaluated}")
        report.append(f"- Pending: {total_tests - evaluated}\n")
        
        # Individual test results
        report.append("## Test Results\n")
        
        for test_id, test in sorted(self.tests.items()):
            report.append(f"### Test {test_id}: {test.claim_text}")
            report.append(f"**Hypothesis**: {test.hypothesis}")
            report.append(f"**Data Points**: {len(test.data_points)}")
            
            if test.result:
                report.append(f"**Result**: {test.result.value}")
                report.append(f"**Confidence**: {test.confidence:.1%}")
            else:
                report.append("**Result**: Not yet evaluated")
            
            if test.data_points:
                report.append("\n**Evidence collected**:")
                for dp in test.data_points[:3]:  # Show first 3
                    report.append(f"- {dp.source} ({dp.quality.value}): {dp.summary[:100]}...")
            
            report.append("")
        
        # Data quality breakdown
        report.append("## Data Quality Distribution")
        high = sum(1 for dp in self.data_points.values() if dp.quality == DataQuality.HIGH)
        medium = sum(1 for dp in self.data_points.values() if dp.quality == DataQuality.MEDIUM)
        low = sum(1 for dp in self.data_points.values() if dp.quality == DataQuality.LOW)
        
        report.append(f"- High Quality: {high}")
        report.append(f"- Medium Quality: {medium}")
        report.append(f"- Low Quality: {low}")
        
        return "\n".join(report)
    
    def save_tests(self):
        """Save all tests and data to JSON"""
        output = {
            'tests': [],
            'summary': {
                'total_tests': len(self.tests),
                'evaluated': sum(1 for t in self.tests.values() if t.result),
                'data_points': len(self.data_points)
            }
        }
        
        for test in self.tests.values():
            test_dict = asdict(test)
            # Convert enums to strings
            if test.result:
                test_dict['result'] = test.result.value
            for dp in test_dict['data_points']:
                if isinstance(dp.get('quality'), DataQuality):
                    dp['quality'] = dp['quality'].value
            output['tests'].append(test_dict)
        
        os.makedirs("analysis", exist_ok=True)
        with open("analysis/empirical-tests.json", 'w') as f:
            json.dump(output, f, indent=2)
        
        # Save report
        report = self.generate_test_report()
        with open("analysis/empirical-test-report.md", 'w') as f:
            f.write(report)
        
        print(f"Saved {len(self.tests)} tests with {len(self.data_points)} data points")

    def add_sample_data(self):
        """Add sample data structure for demonstration"""
        # Example of how to add data when collected
        sample_data = DataPoint(
            id="DP001",
            source="Example Study 2024",
            date="2024-06-15",
            quality=DataQuality.MEDIUM,
            summary="Study shows 15% of office workers can effectively use AI tools for verification",
            url="https://example.com/study",
            raw_data={"percentage": 15, "sample_size": 1000}
        )
        
        # This would contradict the 5% claim
        self.add_data_point("T1", sample_data)


if __name__ == "__main__":
    tester = EmpiricalTester()
    
    # Add sample data for demonstration
    tester.add_sample_data()
    
    # Evaluate tests
    for test_id in tester.tests:
        result, confidence = tester.evaluate_test(test_id)
        print(f"Test {test_id}: {result.value} (confidence: {confidence:.1%})")
    
    # Save results
    tester.save_tests()
    print("Empirical testing framework initialized")
    print("Report saved to analysis/empirical-test-report.md")