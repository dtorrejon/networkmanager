import os


class FilePath:

    def __call__(self, file: str) -> str:
        return self.get_path(file)

    @classmethod
    def get_path(cls, file: str) -> str:
        absolute_file_path = os.path.abspath(file)
        path, python_filename = os.path.split(absolute_file_path)
        return path


if __name__ == '__main__':
    file_path = FilePath()
    # using __call__ function
    #print(f"using __call__ function")
    #print(file_path(__file__))
    #print(f"Instantiaing object")
    #print(FilePath().get_path(__file__))
