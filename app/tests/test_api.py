from datetime import datetime
from ..modules.services import MachineService, PreparationService
import pytz




class TestMachine:
    NB_MACHINES = 2
    ID_MACHINE = "pcwCjNM56YGyxrBPDfEs"

    def test_get_machines(self):
        print("The size of returned list machines is {} whereas it should be {}".format(len(MachineService().get_machines()[1]), self.NB_MACHINES))
        assert len(MachineService().get_machines()[1]) == self.NB_MACHINES

    def test_get_machine_by_id(self):
        print("The id returned is {} whereas it should be {}".format(MachineService().get_machine_by_id(self.ID_MACHINE)[1].id, self.ID_MACHINE))
        assert MachineService().get_machine_by_id(self.ID_MACHINE)[1].id == self.ID_MACHINE


class TestPreparation:
    USER_ID = "9KFeGrJB7mQqMVX4RISBGRgI2oJ3"
    DATE_LAST_PREP = datetime(2021, 6, 23, 10,0,0, tzinfo=pytz.utc)

    def test_get_last_preparation(self):
        last_prep = PreparationService().get_last_preparation(self.USER_ID)[1].last_time
        year,month,day,hour,minute,second,tzinfo = last_prep.year,last_prep.month,last_prep.day,last_prep.hour, last_prep.minute, last_prep.second, last_prep.tzinfo
        print(f"Date return is {last_prep} where it should be {self.DATE_LAST_PREP} ")
        assert datetime(year,month,day,hour,minute,second,tzinfo=tzinfo)== self.DATE_LAST_PREP