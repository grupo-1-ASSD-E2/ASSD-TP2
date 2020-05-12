from BackEnd.BackEnd import BackEnd
import os

backend = BackEnd()

dir_name = "ProgramaPrincipal/BackEnd/Tracks"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".npy"):
        os.remove(os.path.join(dir_name, item))
