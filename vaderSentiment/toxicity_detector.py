# coding: utf-8
"""
Toxicity & Cyberbullying Detector
Detects harmful, toxic, and cyberbullying messages in online content.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class ToxicityDetector:
    """
    Detects toxicity and cyberbullying in text using VADER sentiment analysis
    combined with toxic keyword detection and pattern matching.
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Toxic keywords and phrases
        self.toxic_keywords = {
            'hate': 2.0, 'kill': 2.0, 'stupid': 1.8, 'dumb': 1.7, 'idiot': 2.0,
            'worthless': 1.9, 'loser': 1.5, 'trash': 1.6, 'disgusting': 1.7,
            'scum': 2.0, 'offensive': 1.5, 'pathetic': 1.6, 'weak': 1.2,
            'ugly': 1.4, 'boring': 1.0, 'creepy': 1.5, 'sick': 1.4,
            'die': 1.8, 'death': 1.3, 'burn': 1.6, 'ruin': 1.5,
            'destroy': 1.4, 'fail': 1.0, 'sucks': 1.3, 'bullshit': 1.8,
            'crap': 1.2, 'asshole': 1.9, 'bitch': 1.7, 'bastard': 1.6,
            'damn': 1.1, 'hell': 0.8, 'piss': 1.3, 'cock': 1.2,
            'racist': 2.0, 'sexist': 2.0, 'discriminate': 1.8,
            'abuse': 1.9, 'bully': 1.8, 'harass': 1.8, 'attack': 1.7,
            'threat': 1.9, 'rape': 2.0, 'molest': 2.0, 'assault': 2.0,
            'nerd': 0.8, 'geek': 0.6, 'gay': 0.5,  # context-dependent, lower by default
            'retard': 2.0, 'gay': 0.5, 'queer': 0.5,  # slurs flagged high
        }
        
        # Intensifiers (amplify toxicity)
        self.intensifiers = ['fucking', 'damn', 'very', 'so', 'absolutely', 'extremely']
        
        # Deintensifiers (reduce toxicity)
        self.deintensifiers = ['kind of', 'sort of', 'maybe', 'perhaps', 'a bit']
    
    def detect_toxicity(self, text):
        """
        Detect toxicity in text.
        
        Returns:
            dict: {
                'is_toxic': bool,
                'toxicity_score': float (0-1),
                'severity': str ('low', 'medium', 'high', 'severe'),
                'toxic_words': list,
                'reasons': list,
                'sentiment_scores': dict
            }
        """
        text_lower = text.lower()
        
        # Get sentiment scores
        sentiment_scores = self.analyzer.polarity_scores(text)
        
        # Extract toxic words
        toxic_words = self._find_toxic_words(text_lower)
        
        # Calculate toxicity score
        toxicity_score = self._calculate_toxicity_score(text_lower, sentiment_scores, toxic_words)
        
        # Determine severity
        severity = self._determine_severity(toxicity_score)
        
        # Get reasons for toxicity
        reasons = self._get_reasons(text_lower, sentiment_scores, toxic_words)
        
        is_toxic = toxicity_score >= 0.4
        
        return {
            'is_toxic': is_toxic,
            'toxicity_score': round(toxicity_score, 3),
            'severity': severity,
            'toxic_words': toxic_words,
            'reasons': reasons,
            'sentiment_scores': {k: round(v, 3) for k, v in sentiment_scores.items()}
        }
    
    def _find_toxic_words(self, text_lower):
        """Find all toxic words in the text."""
        found_toxic_words = []
        # Create pattern to match word boundaries
        for toxic_word, score in self.toxic_keywords.items():
            pattern = r'\b' + re.escape(toxic_word) + r'\b'
            if re.search(pattern, text_lower):
                found_toxic_words.append((toxic_word, score))
        return found_toxic_words
    
    def _calculate_toxicity_score(self, text_lower, sentiment_scores, toxic_words):
        """Calculate overall toxicity score."""
        score = 0.0
        
        # 1. Base score from toxic words (40%)
        if toxic_words:
            avg_toxic_score = sum(t[1] for t in toxic_words) / len(toxic_words)
            score += (avg_toxic_score / 2.0) * 0.4  # normalize to 0-1, weight 40%
        
        # 2. Negative sentiment (30%)
        score += sentiment_scores['neg'] * 0.3
        
        # 3. All caps check (10%)
        if self._has_aggressive_caps(text_lower):
            score += 0.15
        
        # 4. Repetitive punctuation (10%)
        if self._has_aggressive_punctuation(text_lower):
            score += 0.1
        
        # 5. Attack/threat patterns (10%)
        if self._has_attack_pattern(text_lower):
            score += 0.15
        
        # Normalize to 0-1
        return min(score, 1.0)
    
    def _has_aggressive_caps(self, text):
        """Check for aggressive use of ALL CAPS."""
        words = text.split()
        if len(words) < 2:
            return False
        
        caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
        return caps_words / len(words) > 0.3
    
    def _has_aggressive_punctuation(self, text):
        """Check for aggressive punctuation like multiple exclamation marks."""
        return bool(re.search(r'[!?]{3,}', text))
    
    def _has_attack_pattern(self, text):
        """Check for attack/threat patterns."""
        attack_patterns = [
            r'you\s+should\s+\w*\s*(die|kill|hurt)',
            r'i\s+hate\s+you',
            r'you\s+\w*\s*(suck|sucks)',
            r'kys|ctb|rope',  # suicide encouragement abbreviations
            r'you\s+\w*\s*(racist|sexist|homophobic)',
        ]
        
        for pattern in attack_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _determine_severity(self, score):
        """Determine severity level based on toxicity score."""
        if score < 0.4:
            return 'clean'
        elif score < 0.6:
            return 'low'
        elif score < 0.75:
            return 'medium'
        elif score < 0.9:
            return 'high'
        else:
            return 'severe'
    
    def _get_reasons(self, text_lower, sentiment_scores, toxic_words):
        """Get reasons explaining the toxicity."""
        reasons = []
        
        if toxic_words:
            reasons.append(f"Contains {len(toxic_words)} toxic word(s): {', '.join([w[0] for w in toxic_words])}")
        
        if sentiment_scores['neg'] > 0.7:
            reasons.append("Very negative sentiment")
        elif sentiment_scores['neg'] > 0.4:
            reasons.append("Negative sentiment detected")
        
        if self._has_attack_pattern(text_lower):
            reasons.append("Detected attack/threat pattern")
        
        if self._has_aggressive_caps(text_lower):
            reasons.append("Aggressive use of CAPS")
        
        if self._has_aggressive_punctuation(text_lower):
            reasons.append("Aggressive repetitive punctuation")
        
        if sentiment_scores['neu'] > 0.8 and len(text_lower) > 20:
            reasons.append("Neutral tone with toxic content")
        
        if not reasons:
            reasons.append("Minor toxicity indicators")
        
        return reasons
    
    def batch_detect(self, texts):
        """Detect toxicity in multiple texts at once."""
        results = []
        for text in texts:
            results.append({
                'text': text,
                'detection': self.detect_toxicity(text)
            })
        return results
    
    def filter_toxic(self, texts, threshold=0.4):
        """Filter out toxic messages above threshold."""
        clean_texts = []
        toxic_texts = []
        
        for text in texts:
            detection = self.detect_toxicity(text)
            if detection['toxicity_score'] >= threshold:
                toxic_texts.append((text, detection))
            else:
                clean_texts.append((text, detection))
        
        return clean_texts, toxic_texts


def main():
    """Demo of toxicity detection."""
    detector = ToxicityDetector()
    
    print("\n" + "="*70)
    print("TOXICITY & CYBERBULLYING DETECTOR - DEMO")
    print("="*70 + "\n")
    
    test_messages = [
        # Clean messages
        "I really enjoyed the movie!",
        "Thank you for your help, you're amazing!",
        "Great job on the project, everyone worked hard.",
        
        # Toxic messages
        "You're so stupid, I hate you!",
        "You should just kill yourself, nobody likes you",
        "This is absolute garbage, you're a complete loser",
        "Go die in a fire, you worthless piece of trash!!!",
        "You're disgusting and pathetic, nobody wants you here",
        
        # Edge cases
        "I'm not happy with this, it's pretty bad",
        "This movie sucks, but the acting was decent",
    ]
    
    print("Testing {} messages...\n".format(len(test_messages)))
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Message {i}]")
        print(f"Text: \"{message}\"")
        print("-" * 70)
        
        result = detector.detect_toxicity(message)
        
        print(f"Toxicity Score: {result['toxicity_score']} | Severity: {result['severity'].upper()}")
        print(f"Status: {'⚠️  TOXIC' if result['is_toxic'] else '✓ CLEAN'}")
        
        if result['toxic_words']:
            print(f"Toxic Words: {', '.join([w[0] for w in result['toxic_words']])}")
        
        print(f"Sentiment Scores: {result['sentiment_scores']}")
        print(f"Reasons:")
        for reason in result['reasons']:
            print(f"  • {reason}")
    
    print("\n" + "="*70)
    print("BATCH FILTERING EXAMPLE")
    print("="*70 + "\n")
    
    sample_comments = [
        "Great job on this amazing article!",
        "You're an idiot and everyone hates you",
        "I disagree with your opinion",
        "I hope you die in a fire, you piece of trash",
        "This needs improvement",
    ]
    
    clean, toxic = detector.filter_toxic(sample_comments, threshold=0.4)
    
    print(f"\n✓ CLEAN COMMENTS ({len(clean)}):")
    for text, detection in clean:
        print(f"  • \"{text}\" (Score: {detection['toxicity_score']})")
    
    print(f"\n⚠️  TOXIC COMMENTS ({len(toxic)}):")
    for text, detection in toxic:
        print(f"  • \"{text}\" (Score: {detection['toxicity_score']}, Severity: {detection['severity']})")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
