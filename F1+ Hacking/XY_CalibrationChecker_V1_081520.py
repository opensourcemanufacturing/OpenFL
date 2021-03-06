from OpenFL import Printer, FLP

#use this for a real printer (comment this line if you plan to use a Dummy Printer):
p=Printer.Printer()

# OR

# uncomment this for Dummy printer (comment out line 4 and line 47, or this will fail):
#p=Printer.DummyPrinter()

# variables (don't change these)
F=FLP
packets = F.Packets()
grid = p.read_grid_table()

if len(p.list_blocks()) >= 0:
	p.delete_block(0)

packets.append(F.LayerStart(0)) # This puts a marker at the beginning of the block to tell the printer the layer is beginning

# Main function
def flpMaker(x, y):
	# first turn off the laser and move to a point
	packets.append(F.LaserPowerLevel(0))
	packets.append(F.XYMove([[x, y, 2000]]))
	# Turn on the laser
	packets.append(F.LaserPowerLevel(32768))
	# adjust the number in the command below if a longer or shorter laser duration is desired. Must be an unsigned 16 bit integer.
	packets.append(F.XYMove([[x, y, 65535]]))
	# uncomment for button press between points
	#packets.append(F.WaitButtonPress("Press The Button!"))
	return packets

# Main Loop
for row in grid:
	for point in row:
		flpMaker(point[0], point[1])

# Send to printer
packets.append(F.LayerDone()) # This puts a marker at the end of the block to tell the printer that the layer is complete
p.write_block_flp(0, packets)

# these are just for troubleshooting/viewing the FLP packet, comment to remove
layer = p.read_block_flp(0)
print(layer)

# uncomment this to print the calibration grid on the printer (will not work with Dummy Printer)
#p.start_printing(0)
