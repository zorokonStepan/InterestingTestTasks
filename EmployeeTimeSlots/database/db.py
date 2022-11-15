class DataBase:
    """Simulation of a class for working with a database"""
    def __init__(self, *args, **kwargs):
        self.connect(*args, **kwargs)
        ...

    def connect(self, *args, **kwargs):
        pass

    def create_tab(self):
        pass

    def create_obj(self, obj):
        pass

    def get_obj(self, obj):
        pass

    def get_all(self):
        pass

    def update_obj(self, obj):
        pass

    def delete_obj(self, obj):
        pass

    def delete_all(self):
        pass

    def disconnect(self):
        pass
