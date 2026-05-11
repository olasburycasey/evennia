"""
Tests for server input functions.
"""

import pickle

import evennia
from evennia.server import inputfuncs
from evennia.utils.test_resources import BaseEvenniaTest


class TestMonitoredInputfunc(BaseEvenniaTest):
    """
    Regressions for monitor/monitored inputfunc handling.
    """

    def test_monitored_payload_is_pickleable(self):
        """
        The monitored payload sent over AMP must not include raw Session objects.
        """

        self.session.puppet = self.char1
        inputfuncs.monitor(self.session, name="location")
        inputfuncs.monitored(self.session)

        sent_session = evennia.SESSION_HANDLER.data_out.call_args.args[0]
        sent_kwargs = evennia.SESSION_HANDLER.data_out.call_args.kwargs
        monitors = sent_kwargs["monitored"][0]
        monitor_kwargs = monitors[0][4]

        self.assertEqual(sent_session, self.session)
        self.assertIn("session", monitor_kwargs)
        self.assertIsInstance(monitor_kwargs["session"], str)
        pickle.dumps((self.session.sessid, sent_kwargs), pickle.HIGHEST_PROTOCOL)


class TestTextInputNickReplacement(BaseEvenniaTest):
    """Test that nick substitution is skipped when player is inside EvEditor."""

    def test_nick_not_replaced_in_eveditor(self):
        """Nick substitution should not apply when EvEditor is active."""
        from unittest.mock import MagicMock, patch

        # Set up a mock session with a puppet that has an active EvEditor
        session = MagicMock()
        session.account = MagicMock()
        puppet = MagicMock()
        puppet.ndb._eveditor = MagicMock()  # EvEditor is active
        session.puppet = puppet

        # Call text() with input that would normally be nick-replaced
        with patch("evennia.server.inputfuncs.cmdhandler") as mock_cmdhandler:
            inputfuncs.text(session, "sending a letter home")
            # The text should reach cmdhandler unchanged
            args, kwargs = mock_cmdhandler.call_args
            self.assertEqual(args[1], "sending a letter home")

    def test_nick_replaced_when_not_in_eveditor(self):
        """Nick substitution should apply normally when EvEditor is not active."""
        from unittest.mock import MagicMock, patch

        session = MagicMock()
        session.account = MagicMock()
        puppet = MagicMock()
        puppet.ndb._eveditor = None  # No EvEditor active
        puppet.nicks.nickreplace.return_value = "say Hello everyone"
        session.puppet = puppet

        with patch("evennia.server.inputfuncs.cmdhandler") as mock_cmdhandler:
            inputfuncs.text(session, "sending a letter home")
            # Nick replacement should have been called
            puppet.nicks.nickreplace.assert_called_once()