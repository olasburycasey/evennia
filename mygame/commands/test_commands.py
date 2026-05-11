from evennia import Command
from evennia.utils.evtable import EvTable

class CmdTestTable(Command):
    """
    Test generating an EvTable.

    Usage:
      testtable
    
    This command generates a sample EvTable and outputs it to the caller.
    """

    key = "testtable"
    aliases = ["tt"]
    locks = "cmd:all()"
    help_category = "Testing"

    def func(self):
        caller = self.caller
        command_1 = "|lcsay This is command 1|ltcommand 1|le"
        command_2 = "|lcsay This is command 2|ltcommand 2|le"
        command_3 = "|lcsay This is command 3|ltcommand 3|le"
        commands = [ command_1, command_2, command_3 ]
        message = " ".join(commands)
        caller.msg(message)
        table = str(EvTable(*commands))
        caller.msg(table)
