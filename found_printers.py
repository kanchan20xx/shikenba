#coding at utf-8


class FoundPrinterInfo:
    def __init__(self, model_name: str, serial_number: str,
                 ip_address: str, service_instance_name: str,
                 find_by: int) -> None:
        self.model_name = model_name
        self.serial_number = serial_number
        self.ip_address = ip_address
        self.service_instance_name = service_instance_name
        self.find_by = find_by


class FoundPrinterLog:
    def __init__(self) -> None:
        self.printers = []
        pass

    def add_printer(self, printer: FoundPrinterInfo):
        found = [p for p in self.printers
                 if p.model_name == printer.model_name
                 and p.serial_number == printer.serial_number]
        if not found:
            self.printers.append(printer)
        return

    def show_list(self):
        for p in self.printers:
            print(p.model_name)


logger = FoundPrinterLog()
printer1 = FoundPrinterInfo(
    "ZZZ",
    "AAA0000",
    "127.0.0.1",
    "ZZZ (AAA0000) (00:00:00)._priter.tcp.local",
    0)
printer2 = FoundPrinterInfo(
    "BBB",
    "BBB0000",
    "127.0.0.1",
    "BBB (BBB0000) (00:00:00)._priter.tcp.local",
    1)
logger.add_printer(printer1)
logger.add_printer(printer2)
logger.add_printer(printer1)
logger.show_list()
