

class IData(object):

    @classmethod
    def is_valid(self) -> bool:
        pass


class Booking_data(IData):

    def __init__(self, **kwargs) -> None:
        pass

    def is_valid(self) -> bool:
        pass


class Maeva_data(IData):

    def __init__(self, **kwargs) -> None:
        pass

    def is_valid(self) -> bool:
        pass


class Campings_data(IData):

    def __init__(self, **kwargs) -> None:
        pass

    def is_valid(self) -> bool:
        pass


class Edomizil_data(IData):

    def __init__(self, **kwargs) -> None:
        pass

    def is_valid(self) -> bool:
        pass
