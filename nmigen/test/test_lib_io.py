from .tools import *
from ..hdl.ast import *
from ..hdl.cd import *
from ..hdl.dsl import *
from ..hdl.rec import *
from ..back.pysim import *
from ..lib.io import *


class PinLayoutSDRTestCase(FHDLTestCase):
    def test_pin_layout_i(self):
        layout_1 = pin_layout(1, dir="i")
        self.assertEqual(layout_1.fields, {
            "i": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="i")
        self.assertEqual(layout_2.fields, {
            "i": (2, DIR_NONE),
        })

    def test_pin_layout_o(self):
        layout_1 = pin_layout(1, dir="o")
        self.assertEqual(layout_1.fields, {
            "o": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="o")
        self.assertEqual(layout_2.fields, {
            "o": (2, DIR_NONE),
        })

    def test_pin_layout_io(self):
        layout_1 = pin_layout(1, dir="io")
        self.assertEqual(layout_1.fields, {
            "i":  (1, DIR_NONE),
            "o":  (1, DIR_NONE),
            "oe": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="io")
        self.assertEqual(layout_2.fields, {
            "i":  (2, DIR_NONE),
            "o":  (2, DIR_NONE),
            "oe": (1, DIR_NONE),
        })


class PinLayoutDDRTestCase(FHDLTestCase):
    def test_pin_layout_i(self):
        layout_1 = pin_layout(1, dir="i", xdr=2)
        self.assertEqual(layout_1.fields, {
            "i0": (1, DIR_NONE),
            "i1": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="i", xdr=2)
        self.assertEqual(layout_2.fields, {
            "i0": (2, DIR_NONE),
            "i1": (2, DIR_NONE),
        })

    def test_pin_layout_o(self):
        layout_1 = pin_layout(1, dir="o", xdr=2)
        self.assertEqual(layout_1.fields, {
            "o0": (1, DIR_NONE),
            "o1": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="o", xdr=2)
        self.assertEqual(layout_2.fields, {
            "o0": (2, DIR_NONE),
            "o1": (2, DIR_NONE),
        })

    def test_pin_layout_io(self):
        layout_1 = pin_layout(1, dir="io", xdr=2)
        self.assertEqual(layout_1.fields, {
            "i0": (1, DIR_NONE),
            "i1": (1, DIR_NONE),
            "o0": (1, DIR_NONE),
            "o1": (1, DIR_NONE),
            "oe": (1, DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="io", xdr=2)
        self.assertEqual(layout_2.fields, {
            "i0": (2, DIR_NONE),
            "i1": (2, DIR_NONE),
            "o0": (2, DIR_NONE),
            "o1": (2, DIR_NONE),
            "oe": (1, DIR_NONE),
        })


class PinTestCase(FHDLTestCase):
    def test_attributes(self):
        pin = Pin(2, dir="io", xdr=2)
        self.assertEqual(pin.width, 2)
        self.assertEqual(pin.dir,   "io")
        self.assertEqual(pin.xdr,   2)


class CRGTestCase(FHDLTestCase):
    def test_basic(self):
        m = Module()
        m.domains += ClockDomain("test")
        m.submodules += CRG(ClockSignal("test"), reset_delay=3)
        rst = Signal()
        m.d.comb += rst.eq(ResetSignal("sync"))

        with Simulator(m) as sim:
            sim.add_clock(1e-6, domain="test")
            def process():
                self.assertEqual((yield rst), 1)
                yield Tick(); yield Delay(1e-8)
                self.assertEqual((yield rst), 1)
                yield Tick(); yield Delay(1e-8)
                self.assertEqual((yield rst), 1)
                yield Tick(); yield Delay(1e-8)
                self.assertEqual((yield rst), 0)

            sim.add_process(process)
            sim.run()
