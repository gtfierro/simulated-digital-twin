import brickschema
from brickschema.namespaces import BRICK, RDFS, RDF
import json
from element_relationship import Element_Relationship_Extractor
import rdflib

def get_brick_type(semantic_info):
    if semantic_info != "":
        return BRICK[semantic_info.split(" ")[-1].split(":")[1]]
    return ""

def get_brick_label(element, semantic_info, brick_type=None):
    ## multiple elements in modelica can be refering to the same brick entity. ex: reaCor and overwriteCor, both refer to VAV "cor"
    element_label = element.split(".")[-1]
    if semantic_info != "" and "." in element:
        tokens = semantic_info.split(" ")
        if len(tokens) == 3:
            brick_label_from_annotation = semantic_info.split(" ")[0]
            if element_label != brick_label_from_annotation:
                brick_label = brick_label_from_annotation
            else:
                brick_label = element_label
        elif len(tokens) == 2:
            brick_label = element_label
            
        brick_label = element.rsplit(".", 1)[0]+"."+brick_label
        brick_label = brick_label.replace(".", "_")

        # if point, add _u to the end of it --> BOPTEST Only
        if brick_type in all_points:
            brick_label = brick_label+"_u"
        if brick_label == "hvac_hvac":
            print(element, semantic_info)
        return brick_label
    
    return element.replace(".", "_")

def add_to_brick_graph(graph, relationship, from_element, to_element):
    if relationship == "feeds":
        inverse_relationship = "isFedBy"
    elif relationship == "hasPoint":
        inverse_relationship = "isPointOf"
    elif relationship == "hasPart":
        inverse_relationship = "isPartOf"
    elif relationship == "isLocationOf":
        inverse_relationship = "hasLocation"
    else: 
        inverse_relationship = ""

    if from_element in graph:
        if relationship in graph[from_element]:
            if to_element not in graph[from_element][relationship]:
                graph[from_element][relationship].append(to_element)
        else:
            graph[from_element][relationship] = [to_element]
    else:
        graph[from_element] = {relationship: [to_element]} 
        
    if to_element in graph:
        if inverse_relationship in graph[to_element]:
            if from_element not in graph[to_element][inverse_relationship]:
                graph[to_element][inverse_relationship].append(from_element)
        else:
            graph[to_element][inverse_relationship] = [from_element]
    else:
        graph[to_element] = {inverse_relationship: [from_element]} 
        
    return graph

modelica_brick_sensor_type_map = {
    'TemperatureTwoPort': BRICK['Temperature_Sensor'],
    'Temperature': BRICK['Temperature_Sensor'],
    'RelativeTemperature': BRICK['Temperature_Sensor'],
    'TemperatureWetBulbTwoPort': BRICK['Temperature_Sensor'],
    'VolumeFlowRate': BRICK['Flow_Sensor'],
    'RelativeHumidity': BRICK['Humditiy_Sensor'],
    'RelativeHumidityTwoPort': BRICK['Humditiy_Sensor'],
    'Pressure': BRICK['Pressure_Sensor'],
    'RelativePressure': BRICK['Pressure_Sensor']
}

modelica_brick_heat_exchanger_type_map = {
    'DryCoilCounterFlow': BRICK['Heating_Coil'],
    'DryCoilDiscretized': BRICK['Heating_Coil'],
    'DryCoilEffectivenessNTU': BRICK['Heating_Coil'], #DryCoil could also be for cooling in some climate zones, could be part of a heat exchanger,
    'WetCoilCounterFlow': BRICK['Cooling_Coil'],
    'WetCoilDiscretized': BRICK['Cooling_Coil'],
    'EvaporatorCondenser': BRICK['Heat_Exchanger'], #look at which side of compressor it is on to decide if it is evaporator or condensor
    'Heater_T': BRICK['Space_Heater'],
}

modelica_brick_actuator_type_map = {
    'Dampers.Exponential': BRICK['Damper'],
    'Dampers.MixingBox': BRICK['Damper'],
    'Dampers.MixingBoxMinimumFlow': BRICK['Damper'],
    'Dampers.PressureIndependent': BRICK['Damper'],
    'Valves.ThreeWayEqualPercentageLinear': BRICK['Valve'], #need more clarity on the brick side for valves
    'Valves.ThreeWayLinear': BRICK['Valve'],
    'Valves.ThreeWayTable': BRICK['Valve'],
    'Valves.TwoWayEqualPercentageLinear': BRICK['Valve'],
    'Valves.TwoWayLinear': BRICK['Valve'],
    'Valves.TwoWayPolynomial': BRICK['Valve'],
    'Valves.TwoWayPressureIndependent': BRICK['Valve'],
    'Valves.TwoWayQuickOpening': BRICK['Valve'],
    'Valves.TwoWayTable': BRICK['Valve']
}

modelica_brick_mover_type_map = { # anything can be pump or fan according to the media
    'FlowControlled_dp': BRICK['Pump'],
    'FlowControlled_m_flow': BRICK['Pump'],
    'SpeedControlled_Nrpm': BRICK['Fan'],
    'SpeedControlled_y': BRICK['Fan']
}

modelica_brick_thermal_zone_type_map = {
    'Detailed.MixedAir': BRICK['HVAC_Zone'],
    'ReducedOrder.EquivalentAirTemperature': BRICK['HVAC_Zone'],
    'ReducedOrder.RC': BRICK['HVAC_Zone'],
    'ReducedOrer.SolarGain': BRICK['HVAC_Zone']
}

modelica_brick_medium_type_map = {
    'Air': BRICK['Air'],
    'Water': BRICK['Water']
}

config_file = "config_boptest.json"
element_extractor = Element_Relationship_Extractor(config_file=config_file)
with open(config_file) as fp:
    config = json.load(fp)

elements, relationships = element_extractor.extract_class_definition()

brick_graph = brickschema.Graph(load_brick=True)
all_points = list(brick_graph.transitive_subjects(object=BRICK['Point'], predicate=RDFS['subClassOf']))
all_zones = list(brick_graph.transitive_subjects(object=BRICK['Zone'], predicate=RDFS['subClassOf']))
all_equipment = list(brick_graph.transitive_subjects(object=BRICK['Equipment'], predicate=RDFS['subClassOf']))
all_systems = list(brick_graph.transitive_subjects(object=BRICK['System'], predicate=RDFS['subClassOf']))


graph = {}
bldg_graph = brickschema.Graph()
BLDG = rdflib.Namespace("urn:bldg/")
bldg_graph.bind("bldg", BLDG)
ref_ns = rdflib.Namespace("https://brickschema.org/schema/Brick/ref#")
bldg_graph.bind("ref", ref_ns)
bacnet_ns = rdflib.Namespace("http://data.ashrae.org/bacnet/2020#")
bldg_graph.bind("bacnet", bacnet_ns)

bldg_graph.add((BLDG["boptest-proxy-device"], rdflib.RDF.type, bacnet_ns['BACnetDevice']))
bldg_graph.add((BLDG["boptest-proxy-device"], bacnet_ns['device-instance'], rdflib.Literal(599)))
        
point_num = 1

for element in elements:
    type_specifier = elements[element]['type_specifier']
    semantic = elements[element].get('semantic', '')
    parent_brick_type = ""
    if '.' in element:
        parent  = element.rsplit(".", 1)[0]
        parent_semantic_info = elements[parent].get("semantic")
        parent_brick_type = get_brick_type(elements[parent].get("semantic"))
        parent_label = get_brick_label(parent, parent_semantic_info, parent_brick_type)

    if semantic != "":
        brick_type = get_brick_type(semantic)
        element_label = get_brick_label(element, semantic, brick_type)
        
        if element_label not in graph:
            graph[element_label] = {
                "type": brick_type
            }
        else:
            graph[element_label]["type"] = brick_type
            
#         print(element, 'a', brick_type)
        
        if brick_type in all_points:
            bldg_graph.add((BLDG[element_label], rdflib.RDF.type, brick_type))
            bacnet_ref = rdflib.BNode()
            bldg_graph.add((BLDG[element_label], ref_ns['hasExternalReference'], bacnet_ref))
            bldg_graph.add((bacnet_ref, bacnet_ns['object-identifier'], rdflib.Literal("analog-value,{}".format(point_num))))
            bldg_graph.add((bacnet_ref, bacnet_ns['object-type'], rdflib.Literal("analog-value")))
            bldg_graph.add((bacnet_ref, bacnet_ns['object-name'], rdflib.Literal(element_label)))
            bldg_graph.add((bacnet_ref, bacnet_ns['objectOf'], BLDG["boptest-proxy-device"]))
            point_num+=1
            
            if parent_brick_type in all_equipment or parent_brick_type in all_zones or parent_brick_type in all_systems:
#                 print(parent, BRICK['hasPoint'], element)
                bldg_graph.add((BLDG[parent_label], BRICK['hasPoint'], BLDG[element_label]))
                graph = add_to_brick_graph(graph=graph, relationship='hasPoint', from_element=parent_label, to_element=element_label)

        if brick_type in all_zones:
            if parent_brick_type in all_zones:
#                 print(parent, BRICK['hasPart'], element)
                bldg_graph.add((BLDG[parent_label], BRICK['hasPart'], BLDG[element_label]))
                graph = add_to_brick_graph(graph=graph, relationship='hasPart', from_element=parent_label, to_element=element_label)
                    
        if brick_type in all_equipment:
            if parent_brick_type in all_equipment or parent_brick_type in all_systems:
#                 print(parent, BRICK['hasPart'], element)
                bldg_graph.add((BLDG[parent_label], BRICK['hasPart'], BLDG[element_label]))
                graph = add_to_brick_graph(graph=graph, relationship='hasPart', from_element=parent_label, to_element=element_label)
                    
        if parent_brick_type in all_zones:
#             print(element, BRICK['hasLocation'], parent)
            bldg_graph.add((BLDG[element_label], BRICK['hasLocation'], BLDG[parent_label]))
            graph = add_to_brick_graph(graph=graph, relationship='isLocationOf', from_element=parent_label, to_element=element_label)
            
        if element in relationships:
            from_element_og = element
            from_element = element
        else:
            for fro in relationships:
                if "." in fro and fro.rsplit(".", 1)[0] == element:
                    from_element_og = fro
                    from_element = fro.rsplit(".", 1)[0]
                    break
        
        for to_element_og in relationships[from_element_og]:
            to_semantic = ""
            to_element = None
            if to_element_og in elements:
                to_element = to_element_og
            elif to_element_og.rsplit(".", 1)[0] in elements:
                to_element = to_element_og.rsplit(".", 1)[0]
            to_semantic = elements[to_element].get('semantic')
            
            if to_semantic != "":
                to_brick_type = get_brick_type(to_semantic)
                from_element_label = get_brick_label(from_element, semantic, brick_type)
                to_element_label = get_brick_label(to_element, to_semantic, to_brick_type)
                
                if brick_type in all_equipment:
                    if to_brick_type in all_equipment:
                        if from_element_og != from_element and to_element_og != to_element:
                            from_port = from_element_og.rsplit(".", 1)[1]
                            to_port = to_element_og.rsplit(".", 1)[1]
                            
                            if (from_port.startswith("port_b") or from_port.startswith("port2") or from_port.startswith("portb") or from_port.startswith("port_2")) and \
                                (to_port.startswith("port_a") or to_port.startswith("port1") or to_port.startswith("porta") or to_port.startswith("port_1")):
#                                 print(from_element, BRICK['feeds'], to_element)
                                bldg_graph.add((BLDG[from_element_label], BRICK['feeds'], BLDG[to_element_label]))
                                
                                graph = add_to_brick_graph(graph=graph, relationship='feeds', from_element=from_element_label, to_element=to_element_label)
                                    
                    if to_brick_type in all_points:
#                         print(from_element, BRICK['hasPoint'], to_element)
                        bldg_graph.add((BLDG[from_element_label], BRICK['hasPoint'], BLDG[to_element_label]))
                        graph = add_to_brick_graph(graph=graph, relationship='hasPoint', from_element=from_element_label, to_element=to_element_label)
#         print("\n")

bldg_graph.serialize(destination=config.get('model').replace('.', '_')+"_brick.ttl", format='turtle')
