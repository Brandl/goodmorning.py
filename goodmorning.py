from escpos.printer import Network

thermal=Network("192.168.0.4") #TODO: make configureable
thermal.text("Hello World\n")
thermal.cut()
