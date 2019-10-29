from device import Device, TouchScreenKeyboardDeviceDirector
from human import Human
from operators import Perceptual, Cognitive, MotorOperator
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import sys

# This is the main function that runs all your  simulations and predicitons.
# Use this to execute your simulation.
# Contributors: nbanovic@umich.edu, jspalt@umich.edu

def draw_scedule_graph(input, schedule_chart):
    ''' Takes in a schedule graph with already executed nodes, then draws nodes based on their type, start times and duration. '''

    LAYER_HEIGHT = 2000

    max_end_time  = 0

    schedule_chart_plot = plt.figure()

    schedule_chart_plot.suptitle(input, fontsize=10)

    ax1 = schedule_chart_plot.add_subplot(111, aspect='equal')
    

    # Calculate positions.
    for operator in nx.topological_sort(schedule_chart):

        # Split nodes in layers.
        if isinstance(operator, Perceptual):
            y = LAYER_HEIGHT
        elif isinstance(operator, Cognitive):
            y = 2*LAYER_HEIGHT
        elif isinstance(operator, MotorOperator):
            y = 3*LAYER_HEIGHT

        ax1.annotate(operator.name, xy=(operator.start_time + operator.duration / 2, y - 3*LAYER_HEIGHT/4 - 50), xytext=(0, 0), textcoords="offset points", ha='center', va='center', color='black', weight='bold', clip_on=True, fontsize=4)
        ax1.add_patch(patches.Rectangle((operator.start_time, y - 3*LAYER_HEIGHT/4), operator.duration , LAYER_HEIGHT/2, fill=True, edgecolor='black', facecolor='gray'))

        # Draw arrows from parents.
        for predecessor in schedule_chart.predecessors(operator):
            if isinstance(predecessor, Perceptual):
                p_y = LAYER_HEIGHT
            elif isinstance(predecessor, Cognitive):
                p_y = 2*LAYER_HEIGHT
            elif isinstance(predecessor, MotorOperator):
                p_y = 3*LAYER_HEIGHT

            ax1.add_patch(patches.Arrow(predecessor.end_time, p_y - LAYER_HEIGHT/2, operator.start_time - predecessor.end_time, y - LAYER_HEIGHT/2 - (p_y - LAYER_HEIGHT/2), width=50))

        if max_end_time <  operator.end_time:
            max_end_time = operator.end_time
        
    ax1.xaxis.set_ticks(range(0, int(max_end_time) + 1000, 1000))
    ax1.yaxis.set_ticks(range(0, 3*LAYER_HEIGHT, 1000))
    
    plt.ylim((0, 3*LAYER_HEIGHT))
    plt.xlim((0, int(max_end_time)))
    ax1.set_ylim(ax1.get_ylim()[::-1]) 

    plt.show(block=True)
    plt.close()
    

def main(argv):

    # Constructs a sample touchscreen device with keyboard at the bottom third of the device.
    device = TouchScreenKeyboardDeviceDirector.construct('device', 'device', 0, 0, 960, 2160, 30, 270)

    # Create a human and associate it with the device, so that the device knows about any body part movements.
    human = Human(device)

    # Create a thumb on the human and place it over the space button to begin with.
    space_key = device.find_descendant(' ')

    human.create_finger('thumb', space_key.top_left_x + space_key.width/2, space_key.top_left_y + space_key.height/2)
    human.create_eyes('eyes', space_key.top_left_x + space_key.width/2, space_key.top_left_y + space_key.height/2, 1000)
    human.create_ltm('ltm') # Long term memory
    human.create_stm('vstm') # Short term memory

    #  Visualize the device interface and the position of the thumb.
    device_plot = plt.figure()
    ax1 = device_plot.add_subplot(111, aspect='equal')
    ax1.xaxis.set_ticks(range(device.top_left_x, device.width, 200))
    ax1.yaxis.set_ticks(range(device.top_left_y, device.height, 200))

    device.draw(ax1)
    human.draw(ax1)
    
    plt.ylim((0, device.height))
    plt.xlim((0, device.width))
    ax1.set_ylim(ax1.get_ylim()[::-1]) 
    ax1.xaxis.tick_top()

    plt.show(block=True)
    plt.close()

    # Variables for computing average typing speed.
    total_characters_count = 0
    total_duration = 0.0

    # For each test phrase in the file compute the duration it takes to type that phrase.
    with open('data/phrases.txt') as phrase_set:
        for phrase in phrase_set:

            phrase = phrase.lower().rstrip()

            # Reset the  thumb to the space before each phrase.
            human.body_parts['thumb'].location_x = space_key.top_left_x + space_key.width/2
            human.body_parts['thumb'].location_y = space_key.top_left_y + space_key.height/2

            schedule_chart = human.press(phrase)

            duration = 0
            for operator in nx.topological_sort(schedule_chart):
                operator.execute()

                # Set start time to predecessors max end time.
                operator.start_time = 0
                for predecessor in schedule_chart.predecessors(operator):
                    if predecessor.end_time > operator.start_time:
                        operator.start_time = predecessor.end_time

                operator.end_time = operator.start_time + operator.duration

                # Assumes a dummy end operator
                duration = operator.end_time
            
            total_characters_count += len(phrase)
            total_duration += duration

            draw_scedule_graph(phrase, schedule_chart)

    # Convert total_duration from milliseconds to seconds.
    total_duration /= 1000.0

    speed_char_per_second = total_characters_count/total_duration

    speed_words_per_minute = speed_char_per_second * 60/5

    print("Typists can enter text at the speed of " + str(speed_words_per_minute) + "WPM.")


if __name__ == "__main__":
    main(sys.argv)







