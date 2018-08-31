import os
import subprocess
import re
import numpy as np

def process_lcs(receptor_pdb, grid_space='1.0', number_of_pockets='3', SSS_threshold='6', surface_density='0.5'):
    result = subprocess.run(["lcs", "-i", receptor_pdb, "-s", grid_space, "-n", number_of_pockets, "-t", SSS_threshold, "-d", surface_density], stdout=subprocess.PIPE)
    fh = open("lcs.out", "wb")
    fh.write(result.stdout)
    fh.close()

def get_orig():
    fh = open("lcs.out", "r")
    for line in fh:
        if line.startswith("Mass center"):
            anchor1 = re.search("\(", line)
            anchor2 = re.search("\)", line)
            center_mass = line[anchor1.end():anchor2.start()]
            xyz_coordinates = center_mass.split(" ")
            x_coordinate = xyz_coordinates[0]
            y_coordinate = xyz_coordinates[1]
            z_coordinate = xyz_coordinates[2]
    fh.close()
    return x_coordinate, y_coordinate, z_coordinate
    
def process_autogrid(receptor_pdb, ligand_pdb, grid_center):
    receptor_pdbqt = receptor_pdb[:receptor_pdb.find(".")] + ".pdbqt"
    ligand_pdbqt = ligand_pdb[:ligand_pdb.find(".")] + ".pdbqt"
    subprocess.run(["pythonsh", "prepare_receptor4.py", "-r", receptor_pdb])
    subprocess.run(["pythonsh", "prepare_ligand4.py", "-l", ligand_pdb])
    subprocess.run(["pythonsh", "prepare_gpf4.py", "-r", receptor_pdbqt, "-l", ligand_pdbqt,"-p", grid_center])
    #subprocess.run(["./autogrid4", "-p"])


if __name__ == "__main__":
    receptor_pdb = input("Please enter the pdb file for the receptor: ")
    ligand_pdb = input("Please enter the pdb file for the ligand: ")
    grid_space = input("Please enter the grid space (unit: angstrom), default:1.0 angstrom ") or "1.0"
    number_of_pockets = input("Please enter the number of pockets, default: 3 ") or "3"
    SSS_threshold = input("Please enter the threshold for SSS event, from 3 to 7, default: 6 ") or "6"
    surface_density = input("Please enter the density (dots/A^2) to calculate the surface vertex, default: 0.5 ") or "0.5"

    process_lcs(receptor_pdb, grid_space, number_of_pockets, SSS_threshold, surface_density)
    
    x_coordinate, y_coordinate, z_coordinate = get_orig()
    grid_center = "gridcenter='" + x_coordinate + "," + y_coordinate + "," + z_coordinate+"'"
    
    process_autogrid(receptor_pdb, ligand_pdb, grid_center)
    print("DONE!")
    
    
    
