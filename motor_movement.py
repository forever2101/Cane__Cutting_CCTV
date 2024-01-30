import serial

class Serial_Wrapper:
	def __init__(self, device, baud=9600):
		self.ser = serial.Serial(device, baud)
	
	def send_data(self, data, expect_confirmation = False, print_confirmation = False):
		self.ser.write(data)
		if expect_confirmation:
			print('\t||| Sent "' + str(data) + '" over serial.')
			rec = self.ser.readline()
			if print_confirmation:
				print('\t||| Received "' + str(rec) + '" over serial. Which "decode().rstrip()"s to \'' + rec.decode('ASCII').rstrip() + '\'')

	def flush_buffer(self):
		self.ser.flushOutput()
		
class Serial_Motor_Control:
	def __init__(self, device='COM4', baud=9600, move_flag='3', stop_flag = '8', pause_flag = '6', cut_flag='5', checkhome_flag='9'):
		self.serial_dev = Serial_Wrapper(device, baud)
		self.move_flag = move_flag
		self.cut_flag = cut_flag
		self.pause_flag = pause_flag
		self.stop_flag = stop_flag
		self.checkhome_flag = checkhome_flag
	
	def move(self, num_increments=1):
		self.serial_dev.send_data(self.move_flag.encode())
		
	def cut(self, num_increments=1):
		self.serial_dev.send_data(self.cut_flag.encode())
	
	def stop(self, num_increments=1):
		self.serial_dev.send_data(self.stop_flag.encode())
	
	def pause(self, num_increments=1):
		self.serial_dev.send_data(self.pause_flag.encode())
	
	def checkhome(self, num_increments=1):
		self.serial_dev.send_data(self.checkhome_flag.encode())
		
	def flush_buffer(self):
		self.serial_dev.flush_buffer()
		