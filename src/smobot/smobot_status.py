"""Class for smobot status."""
"""Example json: {'time': '00:00:00', 'grl': 22, 'fd1': 999, 'fd2': 999, 'err': 999, 'p': 999, 'i': 999, 'd': 999, 'dpr': 999, 'ld': 1, 'set': 220, 'ds': 0, 'sot': 0, 'kp': 110, 'ki': 50, 'kd': 100, 'flg': 0}"""

from enum import Enum, auto

class DeviceState(Enum):
    UNKONWN = -1
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def _missing_(cls, value):
        # Log the unknown value if necessary
        # print(f"Warning: Unknown value '{value}' provided for Color enum.")
        return cls.UNKNOWN


class SmobotStatus:
    """Class for Smobot status."""
    def __init__(
        self, time, grl, fd1, fd2, err, p, i, d, dpr, ld, set, ds, sot, kp, ki, kd, flg
    ):
        """Initialize a status."""
        
        self._status = {
            'time': time,
            'grill_temp': grl,
            'setpoint': set,
            'food_probe_1': fd1,
            'food_probe_2': fd2,
            'damper': dpr,
            'lid': ld,
            'state': ds,
            'sot': sot,
            'flags': flg,

            # PID State/Coeffs
            'err': err,
            'p': p,
            'i': i,
            'd': d,
            'kp': kp,
            'ki': ki,
            'kd': kd,
        }


    @property
    def grill_temp(self):
        return self._status['grill_temp']
    @property
    def setpoint(self):
        return self._status['setpoint'] if self.state == DeviceState.ACTIVE else None
    @property
    def food_probe_1(self):
        return None if self._status['food_probe_1'] == 999 else self._status['food_probe_1']
    @property
    def food_probe_2(self):
        return None if self._status['food_probe_2'] == 999 else self._status['food_probe_2']
    @property
    def damper(self):
        return self._status['damper'] if self.state == DeviceState.ACTIVE else None
    @property
    def lid(self):
        return self._status['lid'] if self.state == DeviceState.ACTIVE else None  
    @property
    def pid_p(self):
        return self._status['p'] if self.state == DeviceState.ACTIVE else None
    @property
    def pid_i(self):
        return self._status['i'] if self.state == DeviceState.ACTIVE else None
    @property
    def pid_d(self):
        return self._status['d'] if self.state == DeviceState.ACTIVE else None


    @property
    def state(self):
        return DeviceState(self._status['state'])

    def raw(self, key):
        if key in self._status:
            return self._status[key]
        
        raise ValueError("Requested key ({}) not present in status message".format(key))
