import os

class Dataset():
    @staticmethod
    def refine_dataset(file_path, file_name):
        
        directory = os.path.dirname(file_path)
        new_file_path = Dataset.get_new_file_path(directory,file_name)
        
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw dataset file not found at: {file_path}")
            
        with open(file_path, "r") as file:
            with open(new_file_path, "w") as f:
                for line in file.readlines():
                    l = line.split(",")
                    
                    if len(l) >= 42: 
                        f.write(Dataset.get_attributes(l)+"\n")
        return new_file_path
    
    @staticmethod
    def get_new_file_path(directory, file_name):  
        os.chdir(directory)
        if os.path.exists(file_name):
            os.remove(file_name)
        return os.path.join(os.getcwd(),file_name)
    
    @staticmethod
    def get_attributes(attribute_list):
        
        index_list = [0,1,2,4,5,6,7,22,23,28,29,30,31,32,33,34,35,36,41]  
        
        index = [1,2,41]
        extrated_attributes = []
        for x in index_list:
            
            value = attribute_list[x].strip() 
            if x in index:
                extrated_attributes.append(Dataset.get_mapping(x,value))
            else:
                extrated_attributes.append(value)
        line = ','.join(extrated_attributes)
        return line

    @staticmethod
    def get_mapping(index, value):
        protocol = {
            'tcp' : '6',
            'udp' : '17',
            'icmp': '1' 
        }
       
        service = {
            'http' : '80',
            'http_443' : '443',
            'domain_u' : '53'
        }
        attack = {
            'normal' : '0',
            'neptune' : '1',
            'back' : '2',
            'apache2' : '3',
            'phf' : '4',
            'saint' : '5',
            'ipsweep' : '6',
            'portsweep' : '7',
            'satan' : '8',
            'nmap' : '9'
        }
        
        if index==1:
            return protocol.get(value, '0') 
        elif index==2:
            return service.get(value, '0') 
        else: 
            if value.endswith("."):
                value = value[:-1]
            return attack.get(value, '0')
