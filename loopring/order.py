from typing import Union
from loopring.util.mappings import Mappings



class Validity:
    
    end: int
    start: int

    def __init__(self, **data) -> None:
        for k in data:
            setattr(self, k, data[k])
    
    def __repr__(self) -> None:
        return f"<end={self.end} start={self.start}>"


class Volume:
    
    base_amount: str
    base_filled: str
    fee: str
    quote_amount: str
    quote_filled: str

    def __init__(self, **data) -> None:
        for k in data:
            if not k.islower():
                setattr(self, Mappings.VOLUME_ATTR_MAPPINGS[k], data[k])
                continue

            setattr(self, k, data[k])
    
    def __repr__(self) -> str:
        return f"<base_amount='{self.base_amount}' " + \
            f"base_filled='{self.base_filled}' fee='{self.fee}' " + \
            f"quote_amount='{self.quote_amount}' quote_filled='{self.quote_filled}'>"



class Order:
    """Shouldn't need to call directly."""

    client_order_id: str
    hash: str
    market: str
    order_type: str
    price: str
    side: str
    status: str
    trade_channel: str
    validity: Validity
    volumes: Volume

    def __init__(self, **data) -> None:
        self.__json = data

        if self.__is_error():
            return

        for k in data:
            if not k.islower():
                setattr(self, Mappings.ORDER_ATTR_MAPPINGS[k], data[k])
            
            elif k == "validity":
                setattr(self, k, Validity(**data[k]))
            
            elif k == "volumes":
                setattr(self, k, Volume(**data[k]))
            
            else:
                setattr(self, k, data[k])
    
    def __repr__(self) -> str:
        if self.__is_error():
            return f"<Incomplete order>"

        return f"<hash='{self.hash}' id='{self.client_order_id}' " + \
            f"side='{self.side}' market='{self.market}' price='{self.price}' " + \
            f"order_type='{self.order_type}' trade_channel='{self.trade_channel}' " + \
            f"status='{self.status}' validity={self.validity} volumes={self.volumes}>"
    
    def __str__(self) -> str:
        if self.__is_error():
            return "Incomplete order object."

        return self.hash
    
    def __is_error(self):
        # On an unsuccessful response, the only data in
        # the dictionary would be "resultInfo" along
        # with an error code.
        return len(self.json) < 2

    @property
    def json(self) -> dict[str, Union[str, dict[str, Union[str, int]]]]:
        """Returns the original data from which the object was initialised.

        Disabling :obj:`Client.handle_errors` will prevent
        exceptions from being raised. On a successful response, you will
        still have an :obj:`~loopring.order.Order` object returned, but in
        the event that an exception occurs, you'll receive a :py:class:`dict`
        containing the raw error response data.
        
        .. seealso:: :class:`~.util.mappings.Mappings.ERROR_MAPPINGS`
            in case you have disabled :obj:`Client.handle_errors`
            and wish to handle the raw error JSON response yourself.

        """
        return self.__json
