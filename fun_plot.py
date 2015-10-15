import tkinter as tk

class FunPlot():
	def __init__(self,root):
		self.canvas = tk.Canvas(root,width=200,height=200,bg="black")
		self.root = root
		self.canvas.pack()
		self._drag_data = {"x": 0, "y": 0, "item": None}
		self.circles = []
		self.lines = {}
		self.lines_to_dots = {}
		self.radius = 10
		self.create_circle(100,100,self.radius,fill="white")

		self.canvas.tag_bind("circle","<ButtonPress-1>",self.OnCirclePress)
		self.canvas.tag_bind("circle", "<ButtonRelease-1>", self.OnCircleRelease)
		self.canvas.tag_bind("circle", "<B1-Motion>", self.OnCircleMotion)
		self.canvas.bind("<ButtonPress-3>",self.OnRightClick)
		self.canvas.bind("<Shift-3>",self.quit)

	def create_circle(self,x,y,r,**kwargs):
		new_circle = self.canvas.create_oval(x-r,y-r,x+r,y+r,tags="circle",**kwargs)
		self.circles.append(new_circle)
		self.lines[str(new_circle)] = []

	def circle_center(self,circle):
		tor = self.canvas.coords(circle)
		return (tor[0] + self.radius,tor[1] + self.radius)

	def connect_dots(self,dot_1,dot_2):
		coords_1 = self.circle_center(dot_1)
		coords_2 = self.circle_center(dot_2)
		new_line = self.canvas.create_line(coords_1[0],coords_1[1],coords_2[0],coords_2[1],fill='gray',width=5)
		self.lines[str(dot_1)].append(new_line)
		self.lines[str(dot_2)].append(new_line)
		self.lines_to_dots[str(new_line)] = [str(dot_1),str(dot_2)]

	def move_line(self,line):
		dots = self.lines_to_dots[str(line)]
		coords_1 = self.circle_center(dots[0])
		coords_2 = self.circle_center(dots[1])
		self.canvas.coords(line,coords_1[0],coords_1[1],coords_2[0],coords_2[1])

	def OnCirclePress(self, event):
		'''Begin drag of an object'''
		# record the item and its location
		item = self.canvas.find_closest(event.x, event.y)[0]
		self.canvas.itemconfig(item, fill="gray")
		self._drag_data["item"] = item
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y

	def OnCircleRelease(self, event):
		'''End drag of an object'''
		self.canvas.itemconfig(self._drag_data["item"], fill="white")
		for line in self.lines[str(self._drag_data["item"])]:
			self.move_line(line)
		# reset the drag information
		self._drag_data["item"] = None
		self._drag_data["x"] = 0
		self._drag_data["y"] = 0

	def OnCircleMotion(self, event):
		'''Handle dragging of an object'''
		self.resize_canvas(event)

		# compute how much this object has moved
		delta_x = event.x - self._drag_data["x"]
		delta_y = event.y - self._drag_data["y"]
		# move the object the appropriate amount
		self.canvas.move(self._drag_data["item"], delta_x, delta_y)
		# record the new position
		self._drag_data["x"] = event.x
		self._drag_data["y"] = event.y	
		for line in self.lines[str(self._drag_data["item"])]:
			self.move_line(line)
	
	def OnRightClick(self,event):
		''' make new object '''
		self.create_circle(event.x,event.y,10,fill='red')
		self.connect_dots(self.circles[-2],self.circles[-1])

	def resize_canvas(self,event):
		# case where x_root or y_root is less than 0
		x = self.root.winfo_x()
		y = self.root.winfo_y()
		if event.x < 0:
			self.canvas.configure(width=int(self.canvas['width'])-event.x + 10)
			x += event.x - 10
			for tag in self.canvas.find_withtag("circle"):
				if tag != self._drag_data["item"]:
					self.canvas.move(tag,10-event.x,0)
		elif event.x > int(self.canvas['width']):
			self.canvas.configure(width=event.x+10)
		if event.y < 0:
			self.canvas.configure(height=int(self.canvas['height'])-event.y + 10)
			y += event.y - 10
			for tag in self.canvas.find_withtag("circle"):
				if tag != self._drag_data["item"]:
					self.canvas.move(tag,0,10-event.y)
		elif event.y > int(self.canvas['height']):
			self.canvas.configure(height=event.y+10)
		self.root.geometry("+%s+%s" % (x, y))

	def quit(self,event):
		self.root.destroy()

root = tk.Tk()
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "black")
root.overrideredirect(True)
fun = FunPlot(root)
root.mainloop()	