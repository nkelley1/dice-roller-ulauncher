import random
import re
from ulauncher.api.client import Client
from ulauncher.api.ui import Item, ItemObject
from ulauncher.api.extension import Extension

class DiceRollerExtension(Extension):
    def __init__(self):
        super(DiceRollerExtension, self).__init__()

    def run(self):
        self.listen("roll")

    def on_query(self, query):
        # Split the input by spaces and process each notation (e.g., '2d6 3d4')
        dice_notations = query.query.strip().lower().split()

        # Validate all the dice notations
        invalid_notations = [notation for notation in dice_notations if not self._is_valid_dice_notation(notation)]
        if invalid_notations:
            return self._error_result(invalid_notations)

        # Roll dice for each valid notation
        results = []
        total_sum = 0
        for notation in dice_notations:
            rolls, total = self._roll_dice(notation)
            results.append(f"Rolls ({notation}): {', '.join(map(str, rolls))} Total: {total}")
            total_sum += total

        # Return all the results in one string
        result = "\n".join(results) + f"\nGrand Total: {total_sum}"

        return Item(
            icon="dice",
            text=result,
            subtext="Press enter to copy result",
            on_enter=self.copy_result_to_clipboard(result)
        )

    def _is_valid_dice_notation(self, notation):
        """Check if the notation matches a valid dice pattern like 2d6, 3d10."""
        return bool(re.match(r'^\d+d\d+$', notation))

    def _roll_dice(self, notation):
        """Roll the dice for a given notation like '2d6' or '3d10'."""
        num_dice, num_sides = map(int, notation.split('d'))
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        return rolls, total

    def _error_result(self, invalid_notations):
        """Return an error message if any notation is invalid."""
        return Item(
            icon="dice",
            text=f"Invalid notation(s): {' '.join(invalid_notations)}",
            subtext="Use format like 2d6, 3d10."
        )

    def copy_result_to_clipboard(self, result):
        """Copy the result to the clipboard when the user presses enter."""
        return lambda item: Client.copy_to_clipboard(result)

if __name__ == "__main__":
    DiceRollerExtension().run()
