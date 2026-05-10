import pytest
from evennia.utils import create
from evennia.scripts.models import ScriptDB


@pytest.mark.django_db
def test_script_restart_persists_active_state():
    """Test that calling start(force_restart=True) on a script
    does not permanently set db_is_active to False.
    """
    # 1. Create a persistent TimeScript using Evennia's internal create wrapper
    s = create.create_script('evennia.utils.gametime.TimeScript',
                             interval=10, start_delay=False, repeats=-1)

    # 2. Check the initial active state (Should be True)
    assert s.is_active is True

    # 3. Simulate what gametime.schedule's at_repeat hook does
    s.start(force_restart=True)

    # 4. Check the state after the force restart
    # Fetch from DB to be absolutely sure
    db_s = ScriptDB.objects.get(id=s.id)
    assert db_s.is_active is True
