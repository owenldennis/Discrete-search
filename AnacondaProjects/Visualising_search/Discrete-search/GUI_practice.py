# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 17:21:18 2020

@author: owen
"""
import queens_search_methods as qsm
import discrete_search as ds
import tkinter as tk


verbose=False

class Square():
    
    def __init__(self,i,j,queen=None):
        self.row=i
        self.column=j
        self.queen=queen
        if self.queen:
            assert self.queen.row == self.row
            assert self.queen.column == self.column
    
    def draw(self,coords,canvas,initialise=True):
        #print("Drawing square {0} {1} with queen status {2}".format(self.row,self.column,self.queen_status))
        
        if (self.row+self.column) %2:
            colour='white'
        else:
            colour='black'
        if verbose:
            print("Drawing inside square object method.  Coords are {0}".format(coords))
            print("My position in the board is {0},{1} and my colour is {2}".format(self.row,self.column,colour))
        if initialise:
            canvas.create_rectangle(*coords,outline='yellow',fill=colour)
        
        if self.queen:
            ### check the queen's location is the same as the square's location
            assert self.queen.row == self.row
            assert self.queen.column == self.column
            #print("Queen currently on square {0} {1}".format(self.row,self.column))
            queen_coords=[coords[0],coords[1],int((coords[2]+coords[0])/2),int((coords[3]+coords[1])/2)]
            canvas.create_rectangle(*queen_coords,fill='yellow')
            canvas.create_text(int((coords[2]+coords[0]-20)/2),int((coords[3]+coords[1]-20)/2),text=str(self.queen.score))
        
    


class Board():
    
    def __init__(self,canvas,rows=8,columns=8):
                
        self.columns=columns
        self.rows=rows
        
        self.reset()
        self.hill_climber = ds.Hill_climber(state=self.nqueens_state.queen_list,
                                            target_func=self.nqueens_state.evaluate_position,
                                            states_generator=self.nqueens_state.one_step_iterator)
        
        # not sure if canvas should be stored or just passed to draw method
        self.canvas = canvas
        self.canvas.update()
        self.height=self.canvas.winfo_height()
        self.width =self.canvas.winfo_width()
       
    def reset(self):
        self.nqueens_state = qsm.NQueens_state(self.rows,self.columns)
        queen_dict=self.nqueens_state.location_dict
        # initialise all squares
        self.squares={(i,j) : Square(i,j,queen_dict.get((i,j))) for i in range(self.rows) for j in range(self.columns)}
        # initialise scores for each queen
        self.nqueens_state.set_queen_scores()
        
        
        

        

    def make_next_move(self):
        move,best=self.hill_climber.climb()
        if move:
            queen=move.queen
            new_row=move.row
            # update location of queen based on move passed from hill climber
            self.squares[(queen.row,queen.column)].queen=None
            self.squares[(new_row,queen.column)].queen=queen
            self.move_string = "Queen on column {0} has moved to row {1}\nNew fitness is {2}\n".format(move.queen.column,move.row,best)       
            move.queen.row=move.row
            self.set_queen_scores()
        else:
            self.move_string="Unable to find a one-move improvement from this position\n"
        return self.move_string
    
    def recentre_coords(self,coords,x_shift,y_shift):
        return [int(coords[0]+x_shift),int(coords[1]+y_shift),
                int(coords[2]+x_shift),int(coords[3]+y_shift)]
   
    
    def draw(self,initialise=True):#,canvas=None):
        
        self.canvas.update()
        self.height=self.canvas.winfo_height()
        self.width =self.canvas.winfo_width()

        square_width=int(self.width/self.columns)-2
        square_height=int(self.height/self.rows)-2
        side_margin=int(self.width-square_width*self.columns/2)
        top_margin=int(self.height-square_height*self.rows/2)
        
        for i in range(self.rows):
            for j in range(self.columns):
                coords=[side_margin+j*square_width,top_margin+i*square_height,
                        side_margin-1+(j+1)*square_width,top_margin-1+(i+1)*square_height]
                # default origin is in the centre of the canvas - reset coordinates to make origin at top left for draw method
                coords=self.recentre_coords(coords,-self.width/2,-self.height/2)
                
                if verbose:
                    print("Drawing square id {0},{1} at coords {2}".format(self.squares[(i,j)].row,self.squares[(i,j)].column,coords))
                self.squares[(i,j)].draw(coords=coords,canvas=self.canvas,initialise=initialise)
        
        
        
        



class Application(tk.Frame):
    def next_move(self):
        self.board_canvas.delete('all')
        #self.text_box.insert(tk.END,"Current fitness is ***\n")
        #self.text_box.update()
        move_string=self.board.make_next_move()
        self.text_box.insert(tk.END,move_string)
        self.board.draw()
        
    def run_to_summit(self):
        pass
    
    def reset_position(self):
        self.board.reset()
        self.text_box.delete(1.0,tk.END)
        self.board.draw()
        

    def createWidgets(self):
        self.QUIT = tk.Button(self.top_frame)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})
        
        self.text_box=tk.Text(self.left_frame,yscrollcommand=True)
        #self.text_box.insert(tk.END,"There is no information yet")
        self.text_box.pack(side=tk.TOP)

        self.start_button = tk.Button(self.top_frame)
        self.start_button["text"] = "Click to make next move"
        self.start_button["command"] = self.next_move       
        self.start_button.pack({"side": "left"}) 
        
        self.reset_button = tk.Button(self.top_frame)
        self.reset_button['text'] = 'Reset to a new random position'
        self.reset_button['command'] = self.reset_position
        self.reset_button.pack(side =tk.LEFT)
        
        
        self.board_canvas= tk.Canvas(self.board_frame,bg='blue')
        self.board_canvas.pack()
        self.board=Board(self.board_canvas,rows=8,columns=8)
        self.board.draw()
        
        

        

    def __init__(self, master=None):
        tk.Frame.__init__(self, master,bg='green')
        self.pack()
        self.top_frame=tk.Frame(self,bg='red')
        self.top_frame.grid(row=0,column=0,padx=10,pady=10)
        self.left_frame=tk.Frame(self,bg='grey')
        self.left_frame.grid(row=1,column=0,padx=10,pady=5)
        self.board_frame=tk.Frame(self,bg='green')
        self.board_frame.grid(row=1,column=1,padx=20,pady=2)
        self.createWidgets()

root = tk.Tk()
root.title("Testing Tkinter GUI")
root.config(bg='skyblue')
app = Application(master=root)
app.mainloop()
root.destroy()




