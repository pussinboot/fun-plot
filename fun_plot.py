import tkinter as tk

class FunPlot():
	def __init__(self,root):
		self.canvas = tk.Canvas(root,width=200,height=200,bg="black")
		self.root = root
		self.create_circle(100,100,10,fill="white")
		self.canvas.pack()
		self._drag_data = {"x": 0, "y": 0, "item": None}

		self.canvas.tag_bind("circle","<ButtonPress-1>",self.OnCirclePress)
		self.canvas.tag_bind("circle", "<ButtonRelease-1>", self.OnCircleRelease)
		self.canvas.tag_bind("circle", "<B1-Motion>", self.OnCircleMotion)
		self.canvas.bind("<ButtonPress-3>",self.OnRightClick)
		self.canvas.bind("<Shift-3>",self.quit)

	def create_circle(self,x,y,r,**kwargs):
		return self.canvas.create_oval(x-r,y-r,x+r,y+r,tags="circle",**kwargs)

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
		# reset the drag information

		self.canvas.itemconfig(self._drag_data["item"], fill="white")
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
	
	def OnRightClick(self,event):
		''' make new object '''
		self.create_circle(event.x,event.y,10,fill='red')

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