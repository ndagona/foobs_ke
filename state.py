class StepTracker:
    def __init__(self, steps):
        self.steps = steps
        self.current = 0

    def next_step(self):
        if self.current < len(self.steps) - 1:
            self.current += 1

    def prev_step(self):
        if self.current > 0:
            self.current -= 1

    def show_progress(self):
        for idx, step in enumerate(self.steps):
            if idx == self.current:
                print(f"> Step {idx + 1}: {step} [CURRENT]")
            else:
                print(f"  Step {idx + 1}: {step}")


if __name__ == "__main__":
    steps = [
        "Initialize migration",
        "Validate data",
        "Transfer records",
        "Verify integrity",
        "Complete migration",
    ]
    tracker = StepTracker(steps)
    tracker.show_progress()
    print("\nMoving to next step...\n")
    tracker.next_step()
    tracker.show_progress()
