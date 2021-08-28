import json


class FoundPrinterInfo:
    def __init__(self, model_name: str, serial_number: str,
                 ip_address: str, service_instance_name: str,
                 find_by: int) -> None:
        self.model_name = model_name
        self.serial_number = serial_number
        self.ip_address = ip_address
        self.service_instance_name = service_instance_name
        self.find_by = find_by


class ReportBuilder:
    def __init__(self) -> None:
        self.printer_array = []

    def add_printer_info(self, src: FoundPrinterInfo):
        self.printer_array.append(self.__format(src))
        return

    def __format(self, src: FoundPrinterInfo):
        formated_printer = {}
        formated_printer["model_name"] = src.model_name
        formated_printer["serial_number"] = src.serial_number
        formated_printer["ipAddressV4"] = src.ip_address
        formated_printer["serviceInstanceName"] = src.service_instance_name
        formated_printer["findBy"] = src.find_by

        return formated_printer

    def write(self):
        report_body = {}
        report_body["version"] = "1.0.0"
        report_body["printers"] = self.printer_array
        return json.dumps(report_body)


builder = ReportBuilder()
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
builder.add_printer_info(printer1)
builder.add_printer_info(printer2)
print(builder.write())
