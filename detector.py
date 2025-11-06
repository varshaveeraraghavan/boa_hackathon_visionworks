"""
Duplicate API Detection Engine
AI-powered system to identify duplicate APIs
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import json

class DuplicateAPIDetector:
    def __init__(self):
        """Initialize the detector with ML model"""
        print("Loading AI model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.api_database = []
        self.embeddings = []
        
    def extract_features(self, api_spec: Dict) -> Dict:
        """Extract relevant features from API specification"""
        return {
            'path': api_spec.get('path', ''),
            'method': api_spec.get('method', ''),
            'description': api_spec.get('description', ''),
            'parameters': api_spec.get('parameters', []),
            'response_schema': api_spec.get('response_schema', {}),
            'domain': api_spec.get('domain', ''),
            'tags': api_spec.get('tags', [])
        }
    
    def calculate_path_similarity(self, path1: str, path2: str) -> float:
        """Calculate similarity between two API paths"""
        # Remove versioning and normalize
        path1_parts = [p for p in path1.split('/') if p and not p.startswith('v')]
        path2_parts = [p for p in path2.split('/') if p and not p.startswith('v')]
        
        # Check for parameter placeholders
        path1_normalized = [p if not (p.startswith('{') or p.startswith(':')) else 'PARAM' 
                           for p in path1_parts]
        path2_normalized = [p if not (p.startswith('{') or p.startswith(':')) else 'PARAM' 
                           for p in path2_parts]
        
        # Calculate Jaccard similarity
        set1 = set(path1_normalized)
        set2 = set(path2_normalized)
        
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_semantic_similarity(self, desc1: str, desc2: str) -> float:
        """Calculate semantic similarity using embeddings"""
        if not desc1 or not desc2:
            return 0.0
            
        emb1 = self.embedder.encode([desc1])
        emb2 = self.embedder.encode([desc2])
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        return float(similarity)
    
    def calculate_structural_similarity(self, api1: Dict, api2: Dict) -> float:
        """Calculate structural similarity based on method, parameters, etc."""
        score = 0.0
        
        # Method similarity (30%)
        if api1.get('method') == api2.get('method'):
            score += 0.3
        
        # Domain similarity (40%)
        if api1.get('domain') == api2.get('domain'):
            score += 0.4
        
        # Parameter overlap (30%)
        params1 = set(api1.get('parameters', []))
        params2 = set(api2.get('parameters', []))
        
        if params1 and params2:
            overlap = len(params1.intersection(params2))
            param_score = overlap / max(len(params1), len(params2))
            score += 0.3 * param_score
        
        return score
    
    def calculate_behavioral_similarity(self, api1: Dict, api2: Dict) -> float:
        """Calculate similarity based on response schemas"""
        schema1 = api1.get('response_schema', {})
        schema2 = api2.get('response_schema', {})
        
        if not schema1 or not schema2:
            return 0.0
        
        keys1 = set(schema1.keys())
        keys2 = set(schema2.keys())
        
        if not keys1 or not keys2:
            return 0.0
        
        intersection = len(keys1.intersection(keys2))
        union = len(keys1.union(keys2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_overall_similarity(self, api1: Dict, api2: Dict) -> Dict[str, float]:
        """Calculate comprehensive similarity score"""
        
        # Path similarity
        path_sim = self.calculate_path_similarity(api1['path'], api2['path'])
        
        # Semantic similarity
        semantic_sim = self.calculate_semantic_similarity(
            api1.get('description', ''),
            api2.get('description', '')
        )
        
        # Structural similarity
        structural_sim = self.calculate_structural_similarity(api1, api2)
        
        # Behavioral similarity
        behavioral_sim = self.calculate_behavioral_similarity(api1, api2)
        
        # Weighted overall score
        overall = (
            0.25 * path_sim +
            0.35 * semantic_sim +
            0.25 * structural_sim +
            0.15 * behavioral_sim
        )
        
        return {
            'overall': round(overall * 100, 2),
            'path': round(path_sim * 100, 2),
            'semantic': round(semantic_sim * 100, 2),
            'structural': round(structural_sim * 100, 2),
            'behavioral': round(behavioral_sim * 100, 2)
        }
    
    def add_api(self, api_spec: Dict):
        """Add an API to the database"""
        features = self.extract_features(api_spec)
        self.api_database.append({**api_spec, 'features': features})
        
        # Generate embedding
        description = api_spec.get('description', api_spec.get('path', ''))
        embedding = self.embedder.encode([description])[0]
        self.embeddings.append(embedding)
    
    def find_duplicates(self, api_spec: Dict, threshold: float = 0.6) -> List[Dict]:
        """Find duplicate APIs for the given API specification"""
        if not self.api_database:
            return []
        
        results = []
        
        for idx, candidate in enumerate(self.api_database):
            # Skip self-comparison
            if candidate.get('id') == api_spec.get('id'):
                continue
            
            # Calculate similarity
            similarity = self.calculate_overall_similarity(api_spec, candidate)
            
            # Filter by threshold
            if similarity['overall'] >= threshold * 100:
                results.append({
                    'api': candidate,
                    'similarity': similarity,
                    'recommendation': self._generate_recommendation(similarity)
                })
        
        # Sort by overall similarity
        results.sort(key=lambda x: x['similarity']['overall'], reverse=True)
        
        return results
    
    def _generate_recommendation(self, similarity: Dict) -> str:
        """Generate actionable recommendation based on similarity score"""
        overall = similarity['overall']
        
        if overall >= 80:
            return "CRITICAL: High duplicate probability. Immediate consolidation recommended."
        elif overall >= 60:
            return "WARNING: Likely duplicate. Review for consolidation opportunity."
        else:
            return "INFO: Possible overlap. Consider for future API rationalization."
    
    def generate_report(self, api_spec: Dict, duplicates: List[Dict]) -> Dict:
        """Generate comprehensive duplicate detection report"""
        
        if not duplicates:
            return {
                'status': 'clean',
                'message': 'No significant duplicates detected',
                'api': api_spec,
                'duplicates': []
            }
        
        # Calculate potential savings
        estimated_savings = len(duplicates) * 5000  # $5k per duplicate
        
        return {
            'status': 'duplicates_found',
            'api': api_spec,
            'summary': {
                'total_duplicates': len(duplicates),
                'critical_duplicates': len([d for d in duplicates if d['similarity']['overall'] >= 80]),
                'estimated_savings': estimated_savings,
                'consolidation_priority': 'High' if len(duplicates) >= 2 else 'Medium'
            },
            'duplicates': duplicates
        }


# Example usage
if __name__ == "__main__":
    detector = DuplicateAPIDetector()
    
    # Sample API database
    sample_apis = [
        {
            'id': 1,
            'path': '/api/v1/users/{id}',
            'method': 'GET',
            'description': 'Retrieve user profile information',
            'parameters': ['id'],
            'response_schema': {'userId': 'string', 'name': 'string', 'email': 'string'},
            'domain': 'user-management'
        },
        {
            'id': 2,
            'path': '/api/user/profile/{userId}',
            'method': 'GET',
            'description': 'Get user profile details',
            'parameters': ['userId'],
            'response_schema': {'id': 'string', 'fullName': 'string', 'emailAddress': 'string'},
            'domain': 'user-management'
        },
        {
            'id': 3,
            'path': '/api/v2/users/fetch',
            'method': 'POST',
            'description': 'Fetch user information by ID',
            'parameters': ['user_id'],
            'response_schema': {'user_id': 'string', 'name': 'string', 'email': 'string'},
            'domain': 'user-management'
        }
    ]
    
    # Add APIs to database
    print("Building API database...")
    for api in sample_apis:
        detector.add_api(api)
    
    # Test with first API
    print("\nAnalyzing API:", sample_apis[0]['path'])
    duplicates = detector.find_duplicates(sample_apis[0], threshold=0.4)
    
    # Generate report
    report = detector.generate_report(sample_apis[0], duplicates)
    
    print("\n" + "="*60)
    print("DUPLICATE DETECTION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))