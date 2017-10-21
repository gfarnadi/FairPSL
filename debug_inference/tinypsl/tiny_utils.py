from __future__ import print_function

def read_link_data(knows_fname, knows_target_fname, likes_fname, lived_fname):
    people_dict = dict()
    people_id_dict = dict()
    
    interest_dict = dict()
    interest_id_dict = dict()
    
    places_dict = dict()
    places_id_dict = dict()
    
    def dict_man(constant_dict, id_dict):
        def str2id(cstr):
            if cstr in constant_dict:
                return constant_dict[cstr]
            id = len(constant_dict)
            constant_dict[cstr] = id
            id_dict[id] = cstr
            return id
        return str2id
    
    people_id = dict_man(people_dict, people_id_dict)
    interest_id = dict_man(interest_dict, interest_id_dict)
    place_id = dict_man(places_dict, places_id_dict)
    
    var_counter = 0
            
    knows_rel = dict()
    with open(knows_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split()
            current_tuple = (people_id(line[0]), people_id(line[1]))
            knows_rel[current_tuple] = (True, 1.0)
            
            
    likes_rel = dict()
    with open(likes_fname) as likes_file:
        for line in likes_file:
            line = line.strip()
            if not line: continue
            line = line.split()            
            current_tuple = (people_id(line[0]), interest_id(' '.join(line[1:-1])))
            likes_rel[current_tuple] = (True, float(line[-1]))
            
    lived_rel = dict()
    with open(lived_fname) as lived_file:
        for line in lived_file:
            line = line.strip()
            if not line: continue
            line = line.split()            
            current_tuple = (people_id(line[0]), place_id(' '.join(line[1:])))
            lived_rel[current_tuple] = (True, 1.0)
            
            
    with open(knows_target_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split()
            current_tuple = (people_id(line[0]), people_id(line[1]))
            knows_rel[current_tuple] = (False, var_counter)
            var_counter += 1
            
    for person in people_id_dict:
        for interest in interest_id_dict:
            current_tuple = (person, interest)
            if not current_tuple in likes_rel:
                likes_rel[current_tuple] = (True, 0.0)
                
    for person in people_id_dict:
        for place in places_id_dict:
            current_tuple = (person, place)
            if not current_tuple in lived_rel:
                lived_rel[current_tuple] = (True, 0.0)
                
    return knows_rel, likes_rel, lived_rel, people_id_dict, interest_id_dict, places_id_dict

def write_link_mpe(knows_fname, people_id_dict, knows_rel, solutions):
    with open(knows_fname, 'w') as k_f:
        for p1 in people_id_dict:
            for p2 in people_id_dict:
                if p1==p2: continue
                (isconst, val) = knows_rel[(p1, p2)]
                if not isconst:
                    val = solutions[val]
                print("'%s','%s',%.16f"%(people_id_dict[p1], people_id_dict[p2], val),file=k_f)

if __name__ == '__main__':
    exit(1)
