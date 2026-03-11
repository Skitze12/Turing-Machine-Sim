import pygame
import math
import sys

"""
Keys (KYS)

/ => floating
// => rounds towards minus infinity

pygame.display.flip(), just updates the changes made to screens

"""

#Initialize pygame
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turing machine for Binary Addition")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
LIGHT_GREY = (211, 211, 211)
GAINSBORO = (220, 220, 220)
DIMGREY = (105, 105, 105)
font = pygame.font.SysFont('arial', size = 30)
font_2 = pygame.font.SysFont('courier',size = 30)
font_3 = pygame.font.SysFont('arial',bold = True, italic = True,size = 30)

# Tape setup
TAPE_SIZE = 101
head_index = math.ceil(TAPE_SIZE/2)

Tapes = {
    "Input_1": ['_']*TAPE_SIZE,
    "Input_2": ['_']*TAPE_SIZE,
    "Output": ['_']*TAPE_SIZE
}

Tape_heads = {
    "Input_1": head_index,
    "Input_2": head_index,
    "Output": head_index
}

Tape_y_positions = {
    "Input_1": 200,
    "Input_2": 300,
    "Output": 400
}

#Animation parameters
cell_width = 60
center_cell_x = width // 2 - cell_width // 2 #center of a box to write at
visible_cells = 5 #How many cells i can see of each tape
steps = 80 #Frames in one second
Delay = 100

#Normal Variables 
Steps = 0
current_state = 'q0'

operation = ""

String_Output = ["Accepted","Rejected"]


#GPT gamme this formula for acceleration and deceleration between switching to and from boxes
def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

#Update each tapes without moving


#Drawing each tape (in 1 frame)
def draw_tapes(offsets=None):
    

    #Since draw_tapes is being used many times in 1 second, I thought why not just use this for closing window (handling)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    screen.fill(LIGHT_GREY)
    
    #offset is essntial for smooth animation
    if offsets is None:
        offsets = {name: 0 for name in Tapes}
    
    for tape_name in Tapes:
        #Step_Label = font_4.render(f"Steps: {Steps}",True,)

        y = Tape_y_positions[tape_name]
        current_offset = offsets.get(tape_name, 0)
        
        #Draw tape label
        label_color = RED if current_offset != 0 else BLACK
        label = font_3.render(f"{tape_name.upper()}", True, label_color)
        screen.blit(label, (50, y))
        
        #Draw tape cells
        for i in range(-visible_cells, visible_cells + 1):
            cell_pos = Tape_heads[tape_name] + i
            if 0 <= cell_pos < len(Tapes[tape_name]):
                cell_x = width // 2 + i * cell_width + current_offset
                
                #Making a square and filling that square with black
                pygame.draw.rect(screen, BLACK, (cell_x, y, cell_width, 50))
                #Drawing its border
                pygame.draw.rect(screen, LIGHT_GREY, (cell_x, y, cell_width, 50), 2)
                
                #Highlight current head position
                if i == 0:
                    highlight_color = GREEN if current_offset != 0 else BLUE
                    pygame.draw.rect(screen, highlight_color, (cell_x - 1, y - 1, cell_width + 1, 52), 4)
                

                #Writing text with white Color
                text = font.render(Tapes[tape_name][cell_pos], True, WHITE)
                screen.blit(text, (cell_x + 20, y + 10))
        
        #Draw head(the arrow thingy)
        head_x = width // 2 + 30
        head_color = RED if current_offset != 0 else BLACK
        pygame.draw.polygon(screen, head_color, [
            (head_x, y - 10),
            (head_x - 10, y - 30),
            (head_x + 10, y - 30)
        ])

    state_text = font.render(f"State: {current_state} ({STATES[current_state]})", True, BLACK)
    screen.blit(state_text, (50, 500))
    
    pygame.display.flip()

def move_head(tape_name, direction):
    """Move a single tape head"""
    offset = 0
    
   
    # Animate movement
    for step in range(steps):
     
            #t is simulating time interval
        t = step / (steps - 1)
        
        
        eased_t = ease_in_out(t)

        #Multiplying by -1 because the tape itself moves left
        offset = eased_t * cell_width * (-1 if direction == "Right" else 1)
        
        draw_tapes({tape_name: offset})
        
        pygame.time.delay(10)
    
    # Update head position after animation
    if direction == "Right":
        Tape_heads[tape_name] += 1
    elif direction == "Left":
        Tape_heads[tape_name] -= 1
    
    draw_tapes()

    
    pygame.time.delay(Delay)

def move_two_heads(tape1, dir1, tape2, dir2):
    """Move two tape heads simultaneously"""
    
    offset1 = 0
    offset2 = 0
    
    #Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        
        # Calculate offsets for both tapes
        offset1 = eased_t * cell_width * (-1 if dir1 == "Right" else 1)
        offset2 = eased_t * cell_width * (-1 if dir2 == "Right" else 1)
        
        draw_tapes({tape1: offset1, tape2: offset2})
        pygame.time.delay(10)
    
    #Update head positions after animation
    if dir1 == "Right":
        Tape_heads[tape1] += 1
    elif dir1 == "Left":
        Tape_heads[tape1] -= 1
        
    if dir2 == "Right":
        Tape_heads[tape2] += 1
    elif dir2 == "Left":
        Tape_heads[tape2] -= 1
    
    draw_tapes()

    pygame.time.delay(Delay)

    
def move_three_heads(tape1, dir1, tape2, dir2, tape3, dir3):
    """Move all three tape heads simultaneously with independent directions"""
    offsets = {tape1: 0, tape2: 0, tape3: 0}
    
    # Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        
        # Calculate offsets for all three tapes
        offsets[tape1] = eased_t * cell_width * (-1 if dir1 == "Right" else 1)
        offsets[tape2] = eased_t * cell_width * (-1 if dir2 == "Right" else 1)
        offsets[tape3] = eased_t * cell_width * (-1 if dir3 == "Right" else 1)
        
        draw_tapes(offsets)
        pygame.time.delay(10)
    
    # Update all head positions after animation
    if dir1 == "Right":
        Tape_heads[tape1] += 1
    elif dir1 == "Left":
        Tape_heads[tape1] -= 1
        
    if dir2 == "Right":
        Tape_heads[tape2] += 1
    elif dir2 == "Left":
        Tape_heads[tape2] -= 1
        
    if dir3 == "Right":
        Tape_heads[tape3] += 1
    elif dir3 == "Left":
        Tape_heads[tape3] -= 1
    
    draw_tapes()

    
    pygame.time.delay(Delay)


def draw_rounded_box(surface, rect, color, border_radius=10, border_color=None, border_width=2):
    pygame.draw.rect(surface, border_color or color, rect, border_radius=border_radius)
    pygame.draw.rect(surface, color, rect.inflate(-border_width*2, -border_width*2), border_radius=border_radius)

def get_input():
    input_text = ""
    active = True
    base_box_width = 400
    input_box_height = 50
    padding = 20

    clock = pygame.time.Clock()

    while active:
        screen.fill(BLACK)

        prompt_text = "Enter two binary digits like (Input1 + Input2) or (Input1 - Input2):"
        promp_render = font.render(prompt_text, True, WHITE)
        input_render = font.render(input_text, True, CYAN)
        prompt_rect = promp_render.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(promp_render, prompt_rect)

        input_width = input_render.get_width()

        #jb input bht sara ho aur base_box_width sy bahr nkl rha ho
        input_box_width = max(base_box_width, input_width + padding * 2)

        input_box_rect = pygame.Rect(0, 0, input_box_width, input_box_height)
        input_box_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        draw_rounded_box(screen, input_box_rect, color=(30, 30, 30), border_radius=10, border_color=CYAN)

        input_text_rect = input_render.get_rect(center=input_box_rect.center)
        screen.blit(input_render, input_text_rect)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    return input_text

def initialize_tape_normal(tape_name,input_str):
    pos = Tape_heads[tape_name]
    for char in input_str:
        Tapes[tape_name][pos] = char
        pos += 1

def initialize_tape_for_subtraction(tape_name, input_str):
    left,right = input_str.split(operation)
    max_len = max(len(left), len(right))

    left = left.zfill(max_len)
    right = right.zfill(max_len)

    result = f"{left}{operation}{right}"

    pos = Tape_heads[tape_name]
    for char in result:
        Tapes[tape_name][pos] = char
        pos += 1


def binary_addition_turing():

    global current_state
    check = False
    if current_state != 'add_q2':
        current_state = 'add_q0'
    else:
        check=True
    while current_state not in ['add_q5', 'add_q_reject']:
        draw_tapes()
        pygame.time.delay(300)
        
        # Get current symbols
        a = Tapes["Input_1"][Tape_heads["Input_1"]]
        b = Tapes["Input_2"][Tape_heads["Input_2"]]
        c = Tapes["Input_2"][Tape_heads["Output"]]

        # State transitions
        if current_state == 'add_q0':
            if a in ['0', '1']:
                move_head("Input_1", "Right")
            elif a == '+':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_head("Input_1", "Right")
                current_state = 'add_q1'
            else:
                current_state = 'add_q_reject'
                
        elif current_state == 'add_q1':
            if a in ['0', '1']:
                Tapes["Input_2"][Tape_heads["Input_2"]] = a
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_two_heads("Input_1", "Right","Input_2", "Right")
            elif a == '_':
                current_state = 'add_q2'
            else:
                current_state = 'add_q_reject'
                
        elif current_state == 'add_q2':
            if a == '_':
                move_head("Input_1", "Left")
            elif a in ['0', '1']:
                move_head("Input_2", "Left")
                current_state = 'add_q3'
        
        elif current_state == 'add_q3':
            if a == '_' and b == '1' and check == True:
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '_'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q5'

            elif a == '1' and b == '1':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '0'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q4'
            
            elif a == '1' and b in ['0','_']:
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'

            elif a in ['0','_'] and b == '1':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'
            
            elif a == '0' and b in ['0','_']:
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '0'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'
            elif a in ['0','_'] and b == '0':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '0'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'

            elif a == '_' and b == '_' and c == '_':
                current_state = 'add_q5'
            
            else:
                current_state = 'add_q_reject'
                
        elif current_state == 'add_q4':
            if a == '1' and b == '1':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q4'
            
            elif a == '1' and b in ['0','_']:
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '0'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q4'

            elif a in ['0','_'] and b == '1':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '0'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q4'

            elif a in ['0','_'] and b == '0':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'
            
            elif a == '0' and b in ['0','_']:
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
                current_state = 'add_q3'


            elif a == '_' and b == '_':
                
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
                Tapes["Output"][Tape_heads["Output"]] = '1'
                current_state = 'add_q5'        
                draw_tapes()
            else:
                current_state = 'add_q_reject'

        if check == False:
            result_text = font.render(
            "Addition Complete!" if current_state == 'add_q5' else "Invalid Input - Rejected!",
            True, GREEN if current_state == 'add_q5' else RED
            )
        else :
            result_text = font.render(
            "Subtraction Complete!" if current_state == 'add_q5' else "Invalid Input - Rejected!",
            True, GREEN if current_state == 'add_q5' else RED
            )
  
    screen.blit(result_text, (width//2 - 150, 550))
    pygame.display.flip()
    pygame.time.delay(2000)




def binary_subtraction_turing():
    global current_state
    current_state = 'sub_q0'

    while current_state not in ['sub_q7', 'sub_q_reject'] or ['add_q2']:
        draw_tapes()
        pygame.time.delay(300)

        a = Tapes["Input_1"][Tape_heads["Input_1"]]
        b = Tapes["Input_2"][Tape_heads["Input_2"]]

        if current_state == 'sub_q0':
            if a in ['0', '1']:
                move_head("Input_1", "Right")
            elif a == '-':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_head("Input_1", "Right")
                current_state = 'sub_q1'
            else:
                current_state = 'sub_q_reject'

        elif current_state == 'sub_q1':
            if a in ['0', '1']:
                flipped = '1' if a == '0' else '0'
                Tapes["Input_2"][Tape_heads["Input_2"]] = flipped
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_two_heads("Input_1", "Right", "Input_2", "Right")
            elif a == '_':
                move_head("Input_2", "Left")
                current_state = 'sub_q2'
            else:
                current_state = 'sub_q_reject'

        elif current_state == 'sub_q2':
            if b == '0':
                Tapes["Input_2"][Tape_heads["Input_2"]] = '1'
                current_state = 'sub_q3'
            elif b == '1':
                Tapes["Input_2"][Tape_heads["Input_2"]] = '0'
                move_head("Input_2", "Left")
            elif b == '_':
                Tapes["Input_2"][Tape_heads["Input_2"]] = '1'
                current_state = 'sub_q3'
            else:
                current_state = 'sub_q_reject'

        elif current_state == 'sub_q3':
            if Tapes["Input_1"][Tape_heads["Input_1"]-1] == '_':
                move_head("Input_1", "Left")
            elif Tapes["Input_1"][Tape_heads["Input_1"]] == '_':
                current_state = 'sub_q4'
            else:
                current_state = 'sub_q_reject'

        elif current_state == 'sub_q4':
            if Tapes["Input_2"][Tape_heads["Input_2"]] in ['0', '1']:
                move_head("Input_2", "Right")
            elif Tapes["Input_2"][Tape_heads["Input_2"]] == '_':
                current_state = 'add_q2'
            else:
                current_state = 'sub_q_reject'

        elif current_state == 'add_q2':
            binary_addition_turing()
            return
    
    # Final display
    pygame.display.flip()
    pygame.time.delay(2000)

STATES = {
    'add_q0': 'Initial scan right',
    'add_q1': 'Copy to tape 2',
    'add_q2': 'Move heads left',
    'add_q3': 'Perform addition',
    'add_q4': 'Add with Carry',
    'add_q5': 'Accept state',
    'add_q_reject': 'Reject state',

    'sub_q0': 'Initial scan right',
    'sub_q1': 'Copy to tape 2',
    'sub_q2': 'Move heads left',
    'sub_q3': 'Perform 2s compliment',
    'sub_q4': 'Moving right of tape 2',
    'sub_q5': 'Perform addition',
    'sub_q6': 'Add with carry',
    'sub_q7': 'Accept state',
    'sub_q_reject': 'Reject state',

    'mul_q0': 'Initial scan right',
    'mul_q1': 'Copy to tape 2',
    'mul_q2': 'Move Input 1 head left',
    'mul_q3': 'Perform multiplication',
    'mul_q4': 'Find spot for 0 tape 2',
    'mul_q5': 'Add 0 to Tape 2',
    'mul_q7': 'Add with Carry',
    'mul_q8': 'Find Spot for Multiplication',
    'mul_q9': "Accept state",
    'mul_q_reject': 'Reject State',
}



def binary_multiplication_turing():
    global current_state 
    current_state = 'mul_q0'

    while current_state not in ['mul_q9','mul_q_reject']:
        draw_tapes()
        pygame.time.delay(300)
        
        #Get current symbols
        a = Tapes["Input_1"][Tape_heads["Input_1"]]
        b = Tapes["Input_2"][Tape_heads["Input_2"]]
        c = Tapes["Output"][Tape_heads["Output"]]
        
        # State transition
        if current_state == 'mul_q0':
        
            if a in ['0','1']:
                move_head("Input_1","Right")
        
            elif a =='*':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_head("Input_1","Right")
                current_state = 'mul_q1'
        
            else:
                current_state = 'mul_q_reject'
        
        elif current_state == 'mul_q1':
            
            if a in ['0','1']:
                Tapes["Input_2"][Tape_heads["Input_2"]] = a
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
                move_two_heads("Input_1","Right","Input_2","Right")

            elif a == '_':
                current_state = 'mul_q2'
            
            else:
                current_state = 'mul_q_reject'
                
        elif current_state == 'mul_q2':

            if a == '_':
                move_head("Input_1","Left")
            
            elif a in ['0','1']:
                move_head("Input_2","Left")
                current_state = 'mul_q3'
                
        elif current_state == 'mul_q3':
            
            if a == '_':
                current_state = 'mul_q9'

            elif a == '0':
                current_state = 'mul_q5'

            elif b == '_' and c == '_':
                move_two_heads("Input_2","Right","Output","Right")
                current_state = 'mul_q4'

            elif a == '1' and c == '_':
                Tapes["Output"][Tape_heads["Output"]] = Tapes["Input_2"][Tape_heads["Input_2"]]
                move_two_heads("Input_2","Left","Output","Left")
            
            elif a == '1' and b == '0' and c in ['0','1']:
                move_two_heads("Input_2","Left","Output","Left")
            
            elif a == '1' and b == '1' and c == '0':
                Tapes["Output"][Tape_heads["Output"]] = Tapes["Input_2"][Tape_heads["Input_2"]]
                move_two_heads("Input_2","Left","Output","Left")
            
            elif a == '1' and b == '1' and c == '1':
                current_state = 'mul_q7'


        elif current_state == 'mul_q4':

            if b == '_':
                current_state = 'mul_q5'
            else:
                move_two_heads('Input_2',"Right","Output","Right")
            
        elif current_state == 'mul_q5':
            
            Tapes["Input_2"][Tape_heads["Input_2"]] = '0'
            move_two_heads('Input_2','Right','Input_1','Left')
            current_state = 'mul_q8'

        elif current_state == 'mul_q7':
            
            if b == '0' and c == '1':
                Tapes["Output"][Tape_heads["Output"]] = "1"
                move_two_heads("Input_2","Left","Output","Left")
                current_state = 'mul_q3'

            elif b == '1' and c == '1':
                Tapes["Output"][Tape_heads["Output"]] = "0"
                move_two_heads("Input_2","Left","Output","Left")
            
            elif b == '1' and c == '_':
                Tapes["Output"][Tape_heads["Output"]] = "0"
                move_two_heads("Input_2","Left","Output","Left")
                                 
            elif b == '_' and c == '_':
                Tapes["Output"][Tape_heads["Output"]] = '1'
                move_two_heads("Input_2","Left","Output","Left")
                move_two_heads("Input_2","Right","Output","Right")
                move_two_heads("Input_2","Right","Output","Right")
                current_state = 'mul_q4'
            
        elif current_state == 'mul_q8':
                if b != '_' and c != '_':
                    move_two_heads("Input_2","Right","Output","Right")
                else:
                    move_two_heads("Input_2","Left","Output","Left")
                    current_state = 'mul_q3'


        result_text = font.render(
            "Multiplication Complete!" if current_state == 'mul_q9' else "Invalid Input - Rejected!",
            True, GREEN if current_state == 'mul_q5' else RED
        )
  
    screen.blit(result_text, (width//2 - 150, 550))
    pygame.display.flip()
    pygame.time.delay(2000)

        
def perform_operation(user_input):
    """Perform the appropriate operation based on the operand"""
    
    if operation == '+':
        initialize_tape_normal("Input_1", user_input)
        binary_addition_turing()
    elif operation == '-':
        initialize_tape_for_subtraction("Input_1", user_input)
        binary_subtraction_turing()
    elif operation == '*':
        initialize_tape_normal("Input_1",user_input)
        binary_multiplication_turing()  # Will implement multiplication later
    else:
        raise ValueError("Unsupported operation")

def set_operation(user_input):
    global operation
    for symbol in user_input:
        if symbol == '+':
            operation = '+'
            break
        elif symbol == '-':
            operation = '-'
            break
        elif symbol =='*':
            operation = '*' 

def main():
    # Get user input
    user_input = get_input()
    
    # Initialize tapes
    set_operation(user_input)
    # Perform the operation
    perform_operation(user_input)

if __name__ == "__main__":
    main()