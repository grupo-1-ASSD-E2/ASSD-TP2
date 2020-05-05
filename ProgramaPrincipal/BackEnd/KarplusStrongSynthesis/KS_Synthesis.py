import numpy as np
import pyaudio
import simpleaudio as sa

def karplus_strong(fs, L, rl, wavetable):
    awgn = np.random.normal(0,1,L+1) # va L+1
    x = awgn
    print('awgn:', awgn)
    print('awgn length:', len(awgn))
    sample_k = 0
    y = []
    for k in range(L):
        sample_k= 0.5 * (x[k+1] + x[k]) + 0.5 * rl * (wavetable[k+1] + wavetable[k])
        y.append(sample_k)
    return np.array(y)

def get_note_signal(fs, note_freq):
    L = int(np.rint((fs / note_freq) - 0.5))
    print ('L:', L)
    wavetable = (2 * np.random.randint(0, 2, L+1) - 1).astype(np.float) #va L+1
    rl = 0.95
    y = karplus_strong(fs, L, rl, wavetable)
    return y


def karplus_strong2(fs, note_freq, N, rl):
    L = int(np.rint((fs / note_freq) - 0.5))
    print ('L:', L)
    wavetable = (2 * np.random.randint(0, 2, L+2) - 1).astype(np.float) #va L+1
    rl = 1
    #awgn = np.random.normal(0,1,N+1) # va L+1
    #x = awgn
    #print('awgn:', awgn)
    #print('awgn length:', awgn.size)
    sample_k = 0
    y = []
    previous_x = np.random.normal(0,1,None)
    print('N.size:')
    print(N.size)
    for k in range(N.size):
        present_x = np.random.normal(0,1,None)
        if k <= L:
            sample_k = 0.5 * (int(present_x) + int(previous_x)) + 0.5 * rl * (int(wavetable[k+1]) + int(wavetable[k]))
            y.append(sample_k)
        else:
            sample_k = 0.5 * (present_x + previous_x) + 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        previous_x = present_x
    y.append(sample_k)
    return np.array(y)



fs = 44100
note_freq = 440
N = np.linspace(0, 1, num=fs)
print('N:')
print(N.size)
rl = 1

#ans = get_note_signal(fs,note_freq)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer=1024,
                output=True,
                output_device_index=2 #A MI ME ANDA CON 2 PERO PUEDE SER QUE A OTRO LE FUNCIONE CON 1!!
                )
ans = karplus_strong2(fs, note_freq, N, rl)
print('ans:')
print(ans.size)
#print(ans)
stream.write(ans.astype(np.float32).tostring())
stream.close()

#audio = ans.astype(np.int16)
#play_obj = sa.play_buffer(audio, 1, 2, fs)
#Wait for playback to finish before exiting
#play_obj.wait_done()
