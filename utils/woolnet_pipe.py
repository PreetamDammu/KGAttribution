import jpype
import jpype.imports
from jpype import JClass, JString, java
from jpype.types import *
import os
import sys


def get_woolnet_paths(node1, node2):
    # Start the JVM
    class_path = "./WD-PathFinder/rdf-entity-path/target/classes"
    jpype.startJVM()


    # Access your Java class 
    curr_path = os.getcwd()
    os.chdir("./WD-PathFinder/rdf-entity-path")
    JavaClass = JClass("com.rdfpath.graph.main.experiments.GetPaths")
    # JavaClass = JClass("GetPaths")
    os.chdir(curr_path)

    # Use the class
    java_instance = JavaClass()
    result = java_instance.getPaths()
    # print(result)

    # Shutdown the JVM
    jpype.shutdownJVM()

    return result