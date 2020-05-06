


class SB_Synthesis:

    def __init__ (self):

    def parabolic_interpolation(self, input_vector, vector_index):
        '''
        Returns the coordinates of the vertex of a parabola that goes through point vector_index and
        its two neighbors.
        '''

        xv = 1/2. * (input_vector[vector_index-1] - input_vector[vector_index+1]) / (input_vector[vector_index-1] - 2 * input_vector[vector_index] + input_vector[vector_index+1]) + vector_index
        yv = input_vector[vector_index] - 1/4. * (input_vector[vector_index-1] - input_vector[vector_index+1]) * (xv - vector_index)
        return (xv, yv)
    
    def get_note_dict(self):
        notes_dictionary = {} 

        start_freq = 16.35 #DO0 will be where the dictionary starts, with a frequency of 16.35Hz
        notes_dictionary["DO0"] = start_freq
        #This will be the list of Notes represented in the letter form
        letters = ["DO#0/REb0", "RE0", "RE#0/MIb0", "MI0", "FA0", "FA#0/SOLb0", "SOL0", "SOL#0/LAb0", "L0", "LA#0/SIb0", "SI0",
                    "DO1", "DO#1/REb1", "RE1", "RE#1/MIb1", "MI1", "FA1", "FA#1/SOLb1", "SOL1", "SOL#1/LAb1", "LA1", "LA#1/SIb1", "SI1",
                    "DO2", "DO#2/REb2", "RE2", "RE#2/MIb2", "MI2", "FA2", "FA#2/SOLb2", "SOL2", "SOL#2/LAb2", "LA2", "LA#2/SIb2", "SI2",
                    "DO3", "DO#3/REb3", "RE3", "RE#3/MIb3", "MI3", "FA3", "FA#3/SOLb3", "SOL3", "SOL#3/LAb3", "LA3", "LA#3/SIb3", "SI3",
                    "DO4", "DO#4/REb4", "RE4", "RE#4/MIb4", "MI4", "FA4", "FA#4/SOLb4", "SOL4", "SOL#4/LAb4", "LA4", "LA#4/SIb4", "SI4",
                    "DO5", "DO#5/REb5", "RE5", "RE#5/MIb5", "MI5", "FA5", "FA#5/SOLb5", "SOL5", "SOL#5/LAb5", "LA5", "LA#5/SIb5", "SI5",
                    "DO6", "DO#6/REb6", "RE6", "RE#6/MIb6", "MI6", "FA6", "FA#6/SOLb6", "SOL6", "SOL#6/LAb6", "LA6", "LA#6/SIb6", "SI6",
                    "DO7", "DO#7/REb7", "RE7", "RE#7/MIb7", "MI7", "FA7", "FA#7/SOLb7", "SOL7", "SOL#7/LAb7", "LA7", "LA#7/SIb7", "SI7",
                    "DO8", "DO#8/REb8", "RE8", "RE#8/MIb8", "MI8", "FA8", "FA#8/SOLb8", "SOL8", "SOL#8/LAb8", "LA8", "LA#8/SIb8", "SI8"] 

        #get an estimate of the next frequency
        for note in letters:
            start_freq = round(start_freq*(2**(1/12)), 2)
            notes_dictionary[note] = start_freq

        return notes_dictionary

