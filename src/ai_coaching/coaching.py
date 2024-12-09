import json

class CoachingEngine:
    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.templates = json.load(f)

    def generate_feedback(self, analysis_results):
        """
        Generate feedback based on analysis results.

        Args:
            analysis_results (dict): The combined analysis results.

        Returns:
            list: List of feedback strings.
        """
        feedback = []

        # Squat correctness feedback
        if not analysis_results['correct_squat']:
            squat_feedback = analysis_results['squat_feedback']
            for issue, message in squat_feedback.items():
                feedback.append(message)
            feedback.append(self.templates['squat']['incorrect'])
        else:
            feedback.append(self.templates['squat']['correct'])

        # Tempo feedback
        average_speed = analysis_results['tempo_results']['average_speed']
        if average_speed < self.templates['tempo']['speed_threshold']:
            feedback.append(self.templates['tempo']['too_slow'])
            feedback.append(self.templates['recommendations']['increase_weight'])
        else:
            feedback.append(self.templates['tempo']['good_speed'])

        # Additional recommendations
        if not analysis_results['correct_squat']:
            feedback.append(self.templates['recommendations']['suggest_stretch'])

        return feedback
