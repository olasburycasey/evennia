import pytest
from evennia.utils import create

@pytest.mark.django_db
def test_script_is_active_after_force_restart():
    """
    Test that a persistent TimeScript remains active after a force restart.
    This verifies the fix for the gametime.schedule persistence bug.
    """
    # 1. Create a persistent TimeScript using Evennia's internal create wrapper
    s = create.create_script('evennia.utils.gametime.TimeScript', interval=10, start_delay=False, repeats=-1)
    
    # 2. Check the initial active state (Should be True)
    assert s.is_active is True
    assert s.db_is_active is True
    
    # 3. Simulate what gametime.schedule's at_repeat hook does
    s.start(force_restart=True)
    
    # 4. Check the state after the force restart
    assert s.is_active is True
    assert s.db_is_active is True
