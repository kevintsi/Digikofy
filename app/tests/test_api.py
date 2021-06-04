from ..modules.services import MachineService
from ..modules.models import Machine



class TestMachine:
    NB_MACHINES = 2
    ID_MACHINE = "pcwCjNM56YGyxrBPDfEs"

    def test_get_machines(self):
        print("The size of returned list machines is {} whereas it should be {}".format(len(MachineService().get_machines()[1]), self.NB_MACHINES))
        assert len(MachineService().get_machines()[1]) == self.NB_MACHINES

    def test_get_machine_by_id(self):
        print("The id returned is {} whereas it should be {}".format(MachineService().get_machine_by_id(self.ID_MACHINE)[1].id, self.ID_MACHINE))
        assert MachineService().get_machine_by_id(self.ID_MACHINE)[1].id == self.ID_MACHINE