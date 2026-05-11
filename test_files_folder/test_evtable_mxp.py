from evennia.utils import evtable, ansi


def test_evtable_mxp_links():
    """
    (Testing fix for Evennia Issue #3082)
    """
    command_1 = "|lcsay This is command 1|ltcommand 1|le"
    command_2 = "|lcsay This is command 2|ltcommand 2|le"
    command_3 = "|lcsay This is command 3|ltcommand 3|le"
    commands1 = [command_1, command_2, command_3]
    # Comparison strings without MXP
    commands2 = ["command 1", "command 2", "command 3"]

    # 1. Verify single cell lengths and contents
    cell1 = ansi.strip_mxp(str(evtable.EvCell(command_1)))
    cell2 = str(evtable.EvCell("command 1"))
    assert cell1 == cell2

    # 2. Verify table with *args
    table1a = ansi.strip_mxp(str(evtable.EvTable(*commands1)))
    table1b = str(evtable.EvTable(*commands2))
    assert table1a == table1b

    # 3. Verify table with kwarg lists
    table2a = ansi.strip_mxp(str(evtable.EvTable(table=[commands1])))
    table2b = str(evtable.EvTable(table=[commands2]))
    assert table2a == table2b

    # 4. Verify that MXP tags SURVIVED inside the EvTable before strip_mxp
    table_str = str(evtable.EvTable(*commands1))
    assert "|lcsay This is command 1|lt" in table_str
