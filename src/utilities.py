class Utilities:
    @staticmethod
    def text_to_binary(text):
        # TODO: Convert text to binary
        pass

    @staticmethod
    def binary_to_text(binary):
        # TODO: Convert binary to text
        pass


def show_progress(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.show_progress:
            print(f"{func.__name__}: {result}")
        return result

    return wrapper
