"""
Rule-based keyword matching classifier (reference implementation)
"""

from typing import Dict, List, Tuple
from .base import DocumentClassifier


class RuleBasedClassifier(DocumentClassifier):
    """
    Rule-based document classifier using keyword matching
    
    This is the reference implementation. Can be replaced with
    ML, LLM, or transformer-based classifiers.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize classifier with rules"""
        self.config = config or {}
        self.rules = self._initialize_rules()
        self.confidence_threshold = self.config.get('classifier', {}).get('confidence_threshold', 0.5)
    
    def _initialize_rules(self) -> Dict[str, Dict[str, any]]:
        """
        Initialize classification rules
        
        Returns:
            Dictionary mapping document types to their rules
        """
        return {
            'Invoice': {
                'required': ['invoice'],
                'strong': ['invoice', 'amount', 'total', 'due', 'bill'],
                'weak': ['payment', 'price', 'cost', 'charge']
            },
            'Contract': {
                'required': ['agreement', 'contract'],
                'strong': ['agreement', 'contract', 'terms', 'conditions', 'party'],
                'weak': ['signed', 'effective', 'date']
            },
            'ID': {
                'required': ['passport', 'license', 'identification'],
                'strong': ['passport', 'driver', 'license', 'identification', 'id number'],
                'weak': ['issued', 'expires', 'birth']
            },
            'BankStatement': {
                'required': ['statement'],
                'strong': ['statement', 'bank', 'account', 'balance', 'transaction'],
                'weak': ['deposit', 'withdrawal', 'credit', 'debit']
            },
            'Receipt': {
                'required': ['receipt'],
                'strong': ['receipt', 'purchased', 'paid', 'transaction'],
                'weak': ['store', 'shop', 'cashier']
            },
            'Resume': {
                'required': ['resume', 'curriculum vitae', 'cv'],
                'strong': ['education', 'experience', 'skills', 'employment'],
                'weak': ['university', 'degree', 'job']
            },
            'Report': {
                'required': ['report'],
                'strong': ['report', 'analysis', 'findings', 'summary', 'conclusion'],
                'weak': ['data', 'results', 'study']
            }
        }
    
    def classify(self, text: str) -> Dict[str, any]:
        """
        Classify document using keyword matching
        
        Args:
            text: Cleaned document text
            
        Returns:
            Classification result with document type and confidence
        """
        if not text:
            return {
                'document_type': 'Unknown',
                'confidence': 0.1
            }
        
        # Normalize text for matching
        text_lower = text.lower()
        
        # Score each document type
        scores = []
        for doc_type, rules in self.rules.items():
            score = self._calculate_score(text_lower, rules)
            scores.append((doc_type, score))
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get best match
        best_type, best_score = scores[0]
        
        # If score is too low, classify as Unknown
        if best_score < self.confidence_threshold:
            return {
                'document_type': 'Unknown',
                'confidence': 0.1
            }
        
        return {
            'document_type': best_type,
            'confidence': round(best_score, 2)
        }
    
    def _calculate_score(self, text: str, rules: Dict[str, List[str]]) -> float:
        """
        Calculate classification score for a document type
        
        Args:
            text: Normalized text
            rules: Classification rules for document type
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 0.0
        
        # Check required keywords (must have at least one)
        required = rules.get('required', [])
        has_required = any(keyword in text for keyword in required)
        if not has_required:
            return 0.0
        
        # Count strong keyword matches
        strong = rules.get('strong', [])
        strong_matches = sum(1 for keyword in strong if keyword in text)
        
        # Count weak keyword matches
        weak = rules.get('weak', [])
        weak_matches = sum(1 for keyword in weak if keyword in text)
        
        # Calculate confidence score
        if strong_matches >= 3:
            score = 0.9  # High confidence
        elif strong_matches >= 2:
            score = 0.7  # Good confidence
        elif strong_matches >= 1:
            score = 0.6  # Moderate confidence
        else:
            score = 0.3  # Low confidence
        
        # Boost for weak matches
        if weak_matches >= 2:
            score = min(1.0, score + 0.1)
        
        return score
