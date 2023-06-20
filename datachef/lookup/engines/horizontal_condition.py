from typing import Callable, Dict

from datachef.models.source.cell import Cell
from datachef.exceptions import BadConditionalResolverError

from ..base import BaseLookupEngine


class HorizontalCondition(BaseLookupEngine):
    """
    A lookup engine to populate the contents of a column based
    on the values resolved for the other columns on the row.
    """
    def __init__(self, label: str, resolver: Callable[[Dict[str, str]], str], priority: int = 0):
        self.label = label
        self.resolver = resolver
        self.priority = priority

    def resolve(self, _: Cell, cells_on_row: Dict[str, str]) -> str:
        """
        For a given observation row (as denoted by the unused Cell argument),
        resolve the  
        """

        if not isinstance(cells_on_row, dict):
            raise BadConditionalResolverError(f'''
                A condition resolver should take an argument of type:
                Dict[str, str] and return type str.
                                              
                The resolver for {self.label} is incorrect, it has
                input_type: {type(cells_on_row)}
                ''')
        
        if any([
            any([not isinstance(x, str) for x in cells_on_row.keys()]),
            any([not isinstance(x, str) for x in cells_on_row.values()])
        ]):
            raise BadConditionalResolverError(f'''
                A condition resolver should take an argument of type:
                Dict[str, str] and return type str.
                                              
                The resolver for {self.label} is incorrect, it has:
                
                keys of type: {set([type(x) for x in cells_on_row.keys()])}
                values of type: {set([type(x) for x in cells_on_row.values()])}
            ''')
            

        try:
            column_value = self.resolver(cells_on_row)
            if not isinstance(column_value, str):
                raise BadConditionalResolverError(f'''
                    A condition resolver should take an argument of type:
                    Dict[str, str] and return type str.
                                                    
                    The resolver for {self.label} is incorrect, it has:

                    return type: {type(column_value)}
                    return value: {column_value} 
                    ''')
            return column_value
        
        except KeyError as err:
            raise Exception(
                f"""
                Unable to resolve lookup for "{self.label}".
                                               
                The column header key "{err.args[0]}" was specified in:
                the condition but is not (yet?) present on the resolved row:
                
                Header Keys: {cells_on_row.keys()}

                Note - please be aware of ordering when using horizontal conditions
                that interact (i.e where condition 2 required condition 1 to be
                resolved first)

                The priority= keyword can be used with the Column.horizontal_condition()
                constructor where conditionals must be sequenced. The lower the priority
                the sooner the condition is executed.
                """
            ) from err
        except Exception as err:
            raise err
