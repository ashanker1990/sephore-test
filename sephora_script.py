import os
import pydot
import re
import sys
import time
from collections import defaultdict



def build_dep():
    ''' Function to build all the dependencies of
    a single sql file in the /tmp folder'''
    
    files_tmp=os.listdir('tmp')
    if len(files_tmp)==0:
        print ("No files exist to construct")
        return None,None
    raw_dep=defaultdict(list)
    tmp_dep=defaultdict(list)
    for file_tmp in files_tmp:
        with open('tmp/'+file_tmp) as fp:
            for line in fp:
                line_raw=line.strip()
                i=0
                while i<=len(line_raw)-3:
                    if line_raw[i]=='r' and line_raw[i+1]=='a' and line_raw[i+2]=='w':
                        line_rest=line_raw[i+4:].split()
                        table_dep=line_rest[0][0:-1]
                        raw_dep['tmp/'+file_tmp[0:-4]].append('raw/'+table_dep)
                    if line_raw[i]=='t' and line_raw[i+1]=='m' and line_raw[i+2]=='p':
                        line_rest=line_raw[i+4:].split()
                        table_dep=line_rest[0][0:-1]
                        tmp_dep['tmp/'+file_tmp[0:-4]].append('tmp/'+table_dep)
                    i+=1
    return raw_dep,tmp_dep

def show_graph(raw_dep,tmp_dep):
    for parent,children in tmp_dep.items():
        print (parent)
        for child in children:
                print ("  --->",child)
                for sub_child in raw_dep[child]:
                    print("     ---->",sub_child)
            

def run_script(s):
    '''Function to simulate a script execution'''
    print (s)
    time.sleep(1)
    return None
    
                    
def run_initial_scripts_parallel(raw_dep,tmp_dep):
    '''Function to simulate parallel execution of a list of scripts'''
    list(map(run_script,[script for script in raw_dep if script not in tmp_dep]) )
    
def recurse_upto_raw_file(raw_dep,tmp_dep,script,parallel_flag):
    '''Function to recurse upto the base script dependancy of a script'''
    if script not in tmp_dep:
        if not parallel_flag:
            run_script(script)
        else:
            pass
    if script in tmp_dep:
        for s in tmp_dep[script]:
            recurse_upto_raw_file(raw_dep,tmp_dep,parallel_flag)
        
        
        
def run_scripts(raw_dep,tmp_dep,parallel_flag):
    '''Function to run the sql scripts in order'''
    for tmp_script in tmp_dep:
        tmp_dependancies=tmp_dep[tmp_script]
        for script in tmp_dependancies:
            recurse_upto_raw_file(raw_dep,tmp_dep,script,parallel_flag)
        print (tmp_script)
        

def main():
    print ("1.Starting to create the dependancy graph")
    raw_dep,tmp_dep=build_dep()
    show_graph(raw_dep,tmp_dep)
    if raw_dep is None and tmp_dep is None:
        sys.exit()
    print ("Dependencies created")
    print ("____________________________________")
    print ("2.Starting script sequence execution:")
    run_scripts(raw_dep,tmp_dep,False)
    print ("Finished script sequence execution....")
    print ("_______________________________________")
    print ("3.Run Initial scripts in parallel")
    run_initial_scripts_parallel(raw_dep,tmp_dep)
    run_scripts(raw_dep,tmp_dep,True)
    print ("Finished script sequence execution....")
    print ("________________________________________")
    
    
    
    

if __name__=='__main__':
    main()
        
    
