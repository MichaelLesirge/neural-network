from button import Button

class Chooser:
    def __init__(self, options: list[Button], default_enabled: int = 0) -> None:
        self.options = options
        
        for button in options:
            button.add_toggle_listener(self.select)

        self.select(options[default_enabled])
    
    def select(self, button: Button) -> None:
        for other_button in self.options:
            other_button.set(other_button == button)

    def get(self):
        for button in self.options:
            if button.get(): return button.get_name()
        raise ValueError("No option selected")